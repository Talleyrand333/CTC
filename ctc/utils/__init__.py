import secrets,string,frappe,http.client,ssl
import qrcode
import json,base64,os,hashlib
import shutil
import time
import random
from frappe.utils import get_files_path
import datetime


def generate_qr_code_and_attach(lab_test):
    #generate qr_code and attach to linked labtest
    try:
        data = get_data(lab_test)
        b64_data = convert_data(data=data)
        file_url = generate_qr_code(b64_data=b64_data,lab_test=lab_test)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(),'QR Code Generation Failed')

    else:
        #send data to cwa api
        send_request_to_server(lab_test)
        return {'file_url':file_url,'lab_test_hash':data.get('hash')}

        frappe.db.commit()

def get_data(lab_test):
    """get data to be sent for generation of qr codes and test results"""
    if not frappe.db.exists('CTC Lab Test',lab_test):
        return
    lab_test = frappe.get_doc('CTC Lab Test',lab_test)
    cwa_option = lab_test.cwa_options
    data = {
        'fn':frappe.db.get_value('CTC Patient',lab_test.patient,'first_name'),
        'ln':frappe.db.get_value('CTC Patient',lab_test.patient,'last_name'),
        'dob':frappe.utils.get_date_str(lab_test.date_of_birth),
        'timestamp':int(lab_test.test_time.timestamp()),
        'testid':lab_test.name,
        'salt':generate_salt()
    }
    ts = datetime.datetime.fromtimestamp(data['timestamp'])
    frappe.log_error(data['timestamp'],'ts1')
    hashed_data = generate_hash(data=data,cwa_option=cwa_option) #hashed data should be stored in labtest as per cwc requirements
    lab_test_hash = frappe.db.set_value('CTC Lab Test',lab_test.name,'lab_test_hash',hashed_data)
    data['hash'] = hashed_data
    if cwa_option == 'Send without Personal Data':
        #remove personal data from keys
        data.pop('fn',None)
        data.pop('ln',None)
        data.pop('dob',None)
        data.pop('testid',None)
    return data

def generate_salt():
    """generate salt of fixed number of 32digit alphanumeric"""
    
    alphabet = string.ascii_uppercase + string.digits
    salt = ''
    for i in range(33):
        salt += secrets.choice(alphabet)
    return salt

def generate_hash(data={},cwa_option=''):
    """generate_hash using request data"""
    if not data:return
    timestamp = str(data['timestamp'])

    if cwa_option == 'Send without Personal Data':
        #send without personal data
        string_value = timestamp + '#' + data['salt']
    if cwa_option == 'Send with Personal Data':
        string_value = data['dob']+ '#' + data['fn'] + '#' + data['ln'] + \
        '#'+ timestamp + '#' + data['testid'] + '#' +  data['salt']
    #get_cwa sending options
    encoded = string_value.encode()
    hash_value = hashlib.sha256(encoded).hexdigest()
    return hash_value

    

def convert_data(data={}):
    """converts the data to base64 encode then to qr code"""
    if not data:return

    str_data = json.dumps(data)
    byte_data = str_data.encode()
    b64_data = base64.b64encode(byte_data).decode()
    return b64_data

def generate_qr_code(b64_data='',lab_test=''):
    from frappe.utils import get_files_path
    """generate qr_code image and attach to lab_test"""
    if not b64_data and lab_test:return
    qr_code_url = frappe.db.get_single_value('CTC Settings','qr_code_url')
    if qr_code_url:
        final_url = qr_code_url + b64_data
        img = qrcode.make(final_url)
        img_name = lab_test + '-' + generate_random() + '.png'
        img.save(img_name) #file saves to the sites folder

        #get cwd of the saved image
        current_path = os.path.realpath('../sites')
        
        source = os.path.join(current_path, img_name)
        destination = os.path.realpath(get_files_path(is_private=1))
        shutil.move(source,destination)
        file_url = '/private/files/' + img_name

        #check if qr codes folder exists and create if not existing
        if not frappe.db.exists('File',{'file_name':'QR Codes','is_folder':1}):
            file = frappe.new_doc("File")
            file.file_name = 'QR Codes'
            file.is_folder = 1
            file.folder = 'Home'
            file.is_private = 1
            file.insert()

            #add the file to QR Codes folder
            file = frappe.new_doc("File")
            file.file_name = img_name
            file.folder = 'Home/QR Codes'
            file.file_url = file_url
            file.insert()

        if frappe.db.exists('File',{'file_name':'QR Codes','is_folder':1}):
            file = frappe.new_doc("File")
            file.file_name = img_name
            file.folder = 'Home/QR Codes'
            file.file_url =  file_url
            file.insert()
        
        #set qr_code_path in labtest
       
        frappe.db.set_value('CTC Lab Test',lab_test,'qr_code_path',file_url)    
        # frappe.db.commit()
        #frappe.db.set_value('CTC Lab Test',lab_test,'lab_test_result','7')    
        return file_url

def generate_random():
    f_string =  ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
    return f_string

########################################################################
def send_request_to_server(lab_test):
    try:
            
        """ send request to ctc testing center """

        from urllib.parse import urlparse
        ctc_settings_doc = frappe.get_doc('CTC Settings')

        #get_full_path of key and certificate files
        cwa_certificate = ctc_settings_doc.cwa_certificate
        cwa_certificate_key = ctc_settings_doc.cwa_certificate_key
        cwa_password = ctc_settings_doc.get_password(fieldname='certificate_passphrase')
        request_url = ctc_settings_doc.ctc_api_url
        if request_url:
            #get host from url
            host = urlparse(request_url).netloc
            
        def get_full_path(file_path):
            if file_path.startswith("/private/files/"):
                file_path = get_files_path(*file_path.split("/private/files/", 1)[1].split("/"), is_private=1)

            if file_path.startswith("/files/"):
                file_path = get_files_path(*file_path.split("/files/", 1)[1].split("/"))

            return os.path.realpath(file_path)
        
        cwa_certificate = get_full_path(cwa_certificate)
        cwa_certificate_key = get_full_path(cwa_certificate_key)

        #prepare connection and send to server
        request_headers = {
            'Content-Type': 'application/json'
        }
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(certfile=cwa_certificate,keyfile=cwa_certificate_key,password=cwa_password)
        connection = http.client.HTTPSConnection(host, port=443, context=context)
    
        #prepare_data
        datalist = []
        data = {}
        data['sc'] = str(int(frappe.db.get_value('CTC Lab Test',lab_test,'test_time').timestamp()))
        ts = data['sc']     
        frappe.log_error(ts,'ts2')

        data['id'] = frappe.db.get_value('CTC Lab Test',lab_test,'lab_test_hash')
        report_result = {'Positive':7,'Negative':6,'Pending':5,'Invalid':8}
        result = frappe.db.get_value('CTC Lab Test',lab_test,'report_status') or 5 #5 means pending
        if result:
            data['result'] =  report_result.get(result)
        else:
            data['result'] = 5 #5 means pending
        datalist.append(data)

        request_data = {}
        request_data['testResults'] = datalist
        
        #send request 
        connection.request(method="POST", url=request_url, headers=request_headers, body=json.dumps(request_data))
        # Print the HTTP response from the CWA service endpoint
        response = connection.getresponse()
        if response.status == 200 or 204:
            
            frappe.msgprint('Data Sent to CWA')
        else:
            frappe.msgprint('Data failed to send to server,please check error logs')
        data = response.read()
    except:
        frappe.log_error(frappe.get_traceback(),'send_request_to_server_failed')