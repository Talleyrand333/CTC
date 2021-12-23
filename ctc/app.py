import frappe
import json

@frappe.whitelist()
def get_patient(**data):
    try:
        if not data.get('patient_name'):
            frappe.local.response['message'] = 'Invalid Data Passed'
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['data'] = {}
        if data.get('patient_name') and frappe.db.exists('CTC Patient',data['patient_name']):
            patient_name = data.get('patient_name')
            patient = frappe.get_doc('CTC Patient', patient_name).as_dict()
            
            frappe.local.response['message'] = 'Patient Retrieved'
            frappe.local.response['http_status_code'] = 200
            frappe.local.response['data'] = patient
        else:
            frappe.local.response['message'] = 'Patient Not Found'
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['data'] = {}
    except:
        frappe.log_error(frappe.get_traceback(),'get_patient_api_call_failed')
        frappe.local.response['message'] = 'Error Retrieving Patient Data'
        frappe.local.response['http_status_code'] = 500
        frappe.local.response['data'] = {}


@frappe.whitelist()
def get_lab_test(**data):
    try:
        if not data.get('lab_test_id'):
            frappe.local.response['message'] = 'Invalid Data Passed'
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['data'] = {}
        if data.get('lab_test_id') and frappe.db.exists('CTC Lab Test',data['lab_test_id']):
            lab_test_id = data.get('lab_test_id')
            lab_test = frappe.get_doc('CTC Lab Test', lab_test_id).as_dict()
            frappe.local.response['message'] = 'Lab Test Retrieved'
            frappe.local.response['http_status_code'] = 200
            frappe.local.response['data'] = lab_test
        else:
            frappe.local.response['message'] = 'Lab Test Not Found'
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['data'] = {}
    except:
        frappe.log_error(frappe.get_traceback(),'get_labtest_api_call_failed')
        frappe.local.response['message'] = 'Error Retrieving Lab Test Data'
        frappe.local.response['http_status_code'] = 500
        frappe.local.response['data'] = {}

@frappe.whitelist()
def get_patients(**data):

    try:
      
        patients = frappe.get_all('CTC Patient', ['name'])
        
        frappe.local.response['message'] = 'Patients Retrieved'
        frappe.local.response['http_status_code'] = 200
        frappe.local.response['data'] = patients
    except:
        frappe.log_error(frappe.get_traceback(),'get_all_patient_api_call_failed')
        frappe.local.response['message'] = 'Error Retrieving Patient Data'
        frappe.local.response['http_status_code'] = 500
        frappe.local.response['data'] = {}

@frappe.whitelist()
def get_lab_tests(**data):

    try:
        lab_tests = frappe.get_all('CTC Lab Test', ['name','patient','creation','status',])
        frappe.local.response['message'] = 'Lab Tests Retrieved'
        frappe.local.response['http_status_code'] = 200
        frappe.local.response['data'] = lab_tests
    except:
        frappe.log_error(frappe.get_traceback(),'get_all_lab_tests_api_call_failed')
        frappe.local.response['message'] = 'Error Retrieving Lab Test Data'
        frappe.local.response['http_status_code'] = 500
        frappe.local.response['data'] = {}

@frappe.whitelist()
def update_patient(**args):
    try:
            
        if args:
            args = frappe._dict(args)
            #update patient 
            name = args.get('patient_name') or args.get('name')
            if frappe.db.exists('CTC Patient',name):
                doc = frappe.get_doc('CTC Patient',name)
                doc.update(args)
                doc.save()
                frappe.db.commit()
                frappe.local.response['message'] = 'patient updated successfully'
                frappe.local.response['http_status_code'] = 200
                
            else:
                frappe.local.response['message'] = 'patient not found in database'
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['data'] = {}
        else:
            frappe.local.response['message'] = 'no data sent'
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['data'] = {}
    except:
        frappe.log_error(frappe.get_traceback(),'update_ctc_patient_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500

@frappe.whitelist()
def update_lab_test(**args):
    try:
            
        if args:
            args = frappe._dict(args)
            #update patient 
            name = args.get('lab_test_id') or args.get('name')
            if frappe.db.exists('CTC Lab Test',name):
                doc = frappe.get_doc('CTC Lab Test',name)
                doc.update(args)
                doc.save()
                frappe.db.commit()
                frappe.local.response['message'] = 'Lab Test updated successfully'
                frappe.local.response['http_status_code'] = 200
                
            else:
                frappe.local.response['message'] = 'Lab Test record not found in database'
                frappe.local.response['http_status_code'] = 404
                frappe.local.response['data'] = {}
        else:
            frappe.local.response['message'] = 'no data sent'
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['data'] = {}
    except:
        frappe.log_error(frappe.get_traceback(),'update_lab_test_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500

@frappe.whitelist()
def create_patient(**args):

    try:
        if args.get('first_name') and args.get('last_name'):
            #create new patient
            patient = frappe.get_doc({
                'doctype':'CTC Patient',
                "first_name": args.get('first_name'),
                "last_name": args.get('last_name'),
                "date_of_birth": args.get('date_of_birth'),
                "full_name": args.get('full_name'),
                "email": args.get('email'),
                "id_number": args.get('id_number'),
                "report_preference": args.get('report_preference'),
                "phone_number": args.get('phone_number'),
                "street": args.get('street'),
                "street_number": args.get('street_number'),
                "zip_code": args.get('zip_code'),
                "towncity": args.get('towncity'),
                "create_lab_test": args.get('create_lab_test'),
                "appointment": args.get('appointment'),
                "test_name": args.get('test_name'),
                "active_subscription": args.get('active_subscription')
            })
            patient.insert()
            frappe.local.response['message'] = 'CTC Patient created successfully'
            frappe.local.response['http_status_code'] = 200
        else:
            frappe.local.response['message'] = 'no data sent'
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['data'] = {}
    except:
        frappe.log_error(frappe.get_traceback(),'create_ctc_patient_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500

@frappe.whitelist()
def create_lab_test(**args):
    try:
        if args.get('location') and args.get('patient'):
            #create new lab_test
            lab_test = frappe.get_doc({
                "doctype":"CTC Lab Test",
                "patient": args.get('patient'),
                "test_name": args.get("test_name"),
                "appointment": args.get('appointment'),
                "send_notification_in_english": args.get('send_notification_in_english'),
                "kundenart": args.get("kundenart"),
                "send_to_cwa": args.get("send_to_cwa"),
                "cwa_options": args.get("cwa_options"),
                "print_on_submit": args.get("print_on_submit"),
                "location": args.get("location"),
                "report_status": args.get("report_status"),
                "report_preference": args.get("report_preference"),
                "test_time": args.get("test_time"),
                #"status": args.get('status'),
                #"full_name": args.get("full_name"),
                #"street": args.get("street"),
                #"zipcode": args.get('zipcode'),
                #"phone_number": args.get("phone_number"),
                #"subscription": args.get("subscription"),
                #"date_of_birth": args.get("date_of_birth"),
                #"street_number": args.get("street_number"),
                #"town": args.get("town"),
                #"email": args.get("email"),
                # "id_number": null,
                # "amended_from": null,
                # "intro_email_sent": 0,
                # "appointment_end": null,
            })
            lab_test.insert()
            frappe.local.response['message'] = 'CTC Lab Test created successfully'
            frappe.local.response['http_status_code'] = 200
        else:
            frappe.local.response['message'] = 'no data sent'
            frappe.local.response['http_status_code'] = 400
            frappe.local.response['data'] = {}
    except:
        frappe.log_error(frappe.get_traceback(),'create_ctc_lab_test_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500

@frappe.whitelist()
def get_location():
    try:
        lab_tests = frappe.get_all('CTC Location', ['name',])
        frappe.local.response['message'] = 'CTC Locations Retrieved'
        frappe.local.response['http_status_code'] = 200
        frappe.local.response['data'] = lab_tests
    except:
        frappe.log_error(frappe.get_traceback(),'get_all_ctc_location_api_call_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500
        frappe.local.response['data'] = {}

@frappe.whitelist()
def send_email(**args):
    try:
        from ctc.corona_test_center.doctype.ctc_lab_test.ctc_lab_test import send_email_to_patient
        if not args.get('name'):
            frappe.local.response['message'] = 'lab test name not in data'
            frappe.local.response['http_status_code'] = 400
        if args.get('name') or args.get('lab_test_id'):
            name = args.get('name') or args.get('lab_test_id')
            if frappe.db.exists('CTC Lab Test',name):
                lab_test = frappe.get_doc('CTC Lab Test',args.get('name'))
                send_email_to_patient(lab_test)
                frappe.local.response['message'] = 'Email Sent to Patient'
                frappe.local.response['http_status_code'] = 200
            else:
                frappe.local.response['message'] = 'Lab Test Not found'
                frappe.local.response['http_status_code'] = 404    
    except:
        frappe.log_error(frappe.get_traceback(),'send_email_to_patient_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500
            
@frappe.whitelist()
def send_sms(**args):
    from ctc.corona_test_center.doctype.ctc_lab_test.ctc_lab_test import send_sms_to_patient
    try:        
        if not args.get('name'):
            frappe.local.response['message'] = 'lab test name not in data'
            frappe.local.response['http_status_code'] = 400
        if args.get('name') or args.get('lab_test_id'):
            name = args.get('name') or args.get('lab_test_id')
            if frappe.db.exists('CTC Lab Test',name):
                lab_test = frappe.get_doc('CTC Lab Test',args.get('name'))
                send_sms_to_patient(lab_test)
                frappe.local.response['message'] = 'SMS Sent to Patient'
                frappe.local.response['http_status_code'] = 200
            else:
                frappe.local.response['message'] = 'Lab Test Not found'
                frappe.local.response['http_status_code'] = 404    
    except:
        frappe.log_error(frappe.get_traceback(),'send_sms_to_patient_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500

@frappe.whitelist()
def send_to_printer(**args):
    from printnode_integration.events import print_via_printnode
    try:        
        if not args.get('name'):
            frappe.local.response['message'] = 'lab test name not in data'
            frappe.local.response['http_status_code'] = 400
        if args.get('name') or args.get('lab_test_id'):
            name = args.get('name') or args.get('lab_test_id')
            if frappe.db.exists('CTC Lab Test',name):
                lab_test = frappe.get_doc('CTC Lab Test',args.get('name'))
                print_via_printnode(doctype='CTC Lab Test',docname=name,docevent='Submit')
                frappe.local.response['message'] = 'Document Sent to Printer'
                frappe.local.response['http_status_code'] = 200
            else:
                frappe.local.response['message'] = 'Lab Test Not found'
                frappe.local.response['http_status_code'] = 404    
    except:
        frappe.log_error(frappe.get_traceback(),'send_sms_to_patient_failed')
        frappe.local.response['message'] = 'Server Error'
        frappe.local.response['http_status_code'] = 500
