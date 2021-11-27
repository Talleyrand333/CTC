# Copyright (c) 2021, Talleyrand and contributors
# For license information, please see license.txt
import datetime,json
import frappe
from frappe import _
from frappe.utils import get_datetime
from frappe.model.document import Document
from six import string_types
import pytz

class CTCLabTest(Document):

    def fetch_api_arguments(self):
        return
        #Fetch all the required information for creating the API
        api_arguments = {}
        api_arguments['fn'] = frappe.get_value("CTC Patient",self.patient,'first_name')
        api_arguments['ln'] = frappe.get_value("CTC Patient",self.patient,'last_name')
        api_arguments['dob']  = frappe.get_value("CTC Patient",self.patient,'date_of_birth').strftime('%Y-%m-%d')
        api_arguments['timestamp'] = str(get_datetime(self.test_time).timestamp())
        api_arguments['test_id'] = self.name
        api_arguments['salt'] = self.generate_code(l=32,is_hex=1)
        api_arguments['hash'] = self.generate_hash(api_arguments)
        return api_arguments
    
    def generate_base64(self,api_args):
        return
        #Generate a base63 encoded character and a QRCode Image for the rest api
        import base64,json,qrcode
        from io import BytesIO
        buffered = BytesIO()
        dumped_json  = json.dumps(api_args)
        encoded_json = base64.b64encode(dumped_json.encode('utf-8'))
        req_url = 'https://s.coronawarn.app?v=1#'+str(encoded_json.decode('UTF-8'))
        print(req_url)
        img = qrcode.make(req_url)
        prop_name = self.name+datetime.date.today().strftime("%Y-%m-%s")+".jpeg"
        save_path = frappe.get_site_path()
        img.save(save_path+"/"+'private/files/'+prop_name,format="JPEG")
        print(save_path+prop_name)
        _file = frappe.get_doc({
                "doctype": "File",
                "file_name":prop_name,
                "attached_to_doctype": self.doctype,
                "attached_to_name": self.name,
                'file_url':'/private/files/'+prop_name,
            })
        _file.flags.ignore_duplicate_entry_error=1
        _file.save(ignore_permissions=True)
        self.qr_code_path = "/"+'private/files/'+prop_name
        # self.save()
        frappe.db.commit()


    def generate_hash(self,api_args):
        import hashlib
        return
        #Generate a Hash256 chracter from a dict of # separated values
        final_stirng = ""
        final_stirng+=api_args['dob']+"#"
        final_stirng+=api_args['fn']+'#'
        final_stirng+=api_args['ln']+"#"
        final_stirng+=api_args['timestamp']+"#"
        final_stirng+=api_args['test_id']+"#"
        final_stirng+=api_args['salt']
        print(final_stirng)
        encoded_fs = final_stirng.encode()
        hash_value = hashlib.sha256(encoded_fs).hexdigest().lower()
        self.hash_content = hash_value
        return hash_value



        

    def autoname(self):
        return
        #Generate a random 7 character string that starts with the letter T
        prop_name = "T"+self.generate_code()
        while frappe.db.exists(self.doctype,prop_name):
            prop_name = "T"+self.generate_code()
        self.name = prop_name
        return
        


    def generate_code(self,l=None,is_hex=True):
        return
        #Generate a string of random characters of the required length and format, it has been defaulted to 6 characters in base 10
        import string,random
        length_= 6 if not l else int(l)
        
        numbers = [str(i) for i in range(10)]
        alpha = string.ascii_letters if not is_hex else 'ABCDEF'
        combined = "".join(numbers)+alpha
        txn_ref = ""
        for i in range(0,length_+1):
            txn_ref+=random.choice(combined)
        txn_=txn_ref
        return(txn_)

    def validate(self):
        api_args = self.fetch_api_arguments()
        #self.generate_base64(api_args)
        if self._action=='submit':
            send_email_to_patient(self)
            send_sms_to_patient(self)

            self.generate_qr_code()
            
    def generate_qr_code(self):
        if self.send_to_cwa and not self.lab_test_hash:
            from ctc.utils import generate_qr_code_and_attach
            generate_qr_code_and_attach(self.name)
    
    def on_cancel(self):
        self.status = "Cancelled"


    def before_submit(self):
        # self.fetch_date()
        self.set_appointment_end()
        
    

    def set_appointment_end(self):
        from frappe.utils import get_datetime
        if self.appointment:
            appointment_end = get_datetime(self.appointment) + datetime.timedelta(minutes=5)
            self.appointment_end=appointment_end

    

    def fetch_date(self):
        #Crude implementation
        tz = pytz.timezone('Europe/Berlin')
        now=datetime.datetime.now(tz)
        self.test_time = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)

@frappe.whitelist()
def fetch_patient_status(doc):
    import datetime
    if isinstance(doc,string_types):
        doc = json.loads(doc)
        doc= frappe.get_doc(doc)
    active = False
    existing_subs = frappe.get_all("Patient Subscription",{'patient':doc.patient},['start_date','end_date'])
    today = datetime.datetime.now()
    if existing_subs:
        for each in existing_subs:
            if get_datetime(each['start_date']) <= today and get_datetime(each['end_date']) > today:
                active = True
    return active
    

@frappe.whitelist()
def send_sms_to_patient(doc):
    from frappe.core.doctype.sms_settings.sms_settings import send_sms
    if isinstance(doc,string_types):
        doc = json.loads(doc)
        doc= frappe.get_doc(doc)
    if doc.report_preference=="SMS" and doc.report_status!='Faulty':
        template = frappe.get_doc("CTC Settings")
        if not(template.get('positive_sms') or template.get('negative_sms')):
            frappe.throw(_("Please ensure that all template fields in CTC Settings page are filled"))
        positive = template.positive_sms 
        positive2 = None if not doc.send_notification_in_english else template.positive_english_sms
        negative = template.negative_sms 
        negative2 = None if not doc.send_notification_in_english else template.negative_english_sms
        data = vars(doc)
        date_ = get_datetime(doc.test_time)
        formated_date = datetime.datetime.strftime(date_,"%d.%m.%Y")
        data['formated_date']=formated_date
        message = positive if doc.report_status =="Positive" else negative
        message=frappe.render_template(message,data)
        send_sms(receiver_list = [doc.phone_number],msg=message)
        if positive2 and negative2:
            message2 = message = positive2 if doc.report_status =="Positive" else negative2
            message2=frappe.render_template(message2,data)
            send_sms(receiver_list = [doc.phone_number],msg=message2)
        return True
        



@frappe.whitelist()
def send_email_to_patient(doc):
    if isinstance(doc,string_types):
        doc = json.loads(doc)
        doc= frappe.get_doc(doc)
    if doc.report_preference=="Email" and doc.report_status!='Faulty':
        template = frappe.get_doc("CTC Settings")
        if not(template.get('postive_email_template') or template.get('negative_email_template')):
            frappe.throw(_("Please ensure that all template fields in CTC Settings page are filled"))
        positive = frappe.get_doc("Email Template",template.positive_email_template) 
        positive2 = None if not doc.send_notification_in_english else frappe.get_doc("Email Template",template.positive_english_template)
        negative = frappe.get_doc("Email Template",template.negative_email_template) 
        negative2=None if not doc.send_notification_in_english else frappe.get_doc("Email Template",template.negative_english_template) 
        data = vars(doc)
        date_ = get_datetime(doc.test_time)
        formated_date = datetime.datetime.strftime(date_,"%d.%m.%Y")
        data['formated_date']=formated_date
        message = positive if doc.report_status =="Positive" else negative
        
        email_args = {
                "recipients": [doc.email],
                "message": frappe.render_template(message.response,data),
                "subject": message.subject,
                "attachments": [frappe.attach_print("CTC Lab Test", doc.name)],
                "reference_doctype": doc.doctype,
                "reference_name": doc.name
                
        }
        
        frappe.sendmail(recipients=email_args['recipients'],
        message=email_args['message'],
        subject=email_args['subject'],
        attachments=email_args['attachments'],
        reference_doctype=doc.doctype,
        reference_name=doc.name)
        if negative2 and positive2:
            message2=  positive2 if doc.report_status =="Positive" else negative2
            email_args['attachments2'] = [frappe.attach_print('CTC Lab Test',doc.name,file_name=doc.name,print_format=template.print_format_for_english_notification)]
            email_args['eng_msg'] = frappe.render_template(message2.response,data)
            email_args['eng_sub'] = message2.subject
            
            frappe.sendmail(
            recipients=email_args['recipients'],
            message=email_args['eng_msg'],
            subject=email_args['eng_sub'],
            attachments=email_args['attachments2'],
            reference_doctype=doc.doctype,
            reference_name=doc.name)
        return True