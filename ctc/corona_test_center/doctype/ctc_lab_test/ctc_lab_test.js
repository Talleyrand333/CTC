// Copyright (c) 2021, Talleyrand and contributors
// For license information, please see license.txt

frappe.ui.form.on('CTC Lab Test', {

	patient: function(frm){
		frappe.call({
			method:'ctc.corona_test_center.doctype.ctc_lab_test.ctc_lab_test.fetch_patient_status',
			args: {
				'doc':frm.doc
			},
			callback:r=>{
				r.message['active'] == true ? frm.doc.subscription = "Active":frm.doc.subscription = "Inactive"
				frm.set_value('report_preference',r.message['default_report_preference'])
				//frm.set_value('location',r.message['location'])
				
				frm.refresh_field('subscription')
				frm.refresh_field('report_preference')
				frm.refresh_field('location')

			}
		})
	},
	refresh: function(frm) {
		if ((!frm.is_new()) && (frm.doc.docstatus==1) ) {
			frm.add_custom_button(__("Send Email"),()=>{
				
				frappe.call({
					method: 'ctc.corona_test_center.doctype.ctc_lab_test.ctc_lab_test.send_email_to_patient',
					args:{
						'doc':cur_frm.doc,
					},
					callback: function() {
						frappe.msgprint({
							title: __('Email'),
							indicator: 'green',
							message: __('Email Sent successfully')
						});
						d.hide();
					}
				});
			})
			frm.add_custom_button(__("Send SMS"),()=>{
				// var number = frm.doc.phone_number;
				// var message = 'Your Test Result ID: ' + frm.doc.name + ' Test Name: ' + frm.doc.test_name + ' and Result :' + frm.doc.report_status + '';
			
				// if (!number || !message) {
				// 	frappe.throw(__('Did not send SMS, missing patient mobile number or message content.'));
				// }
				frappe.call({
					method: 'ctc.corona_test_center.doctype.ctc_lab_test.ctc_lab_test.send_sms_to_patient',
					args: {
						'doc':cur_frm.doc
					},
					callback: function (r) {
						frappe.msgprint({
							title: __('SMS'),
							indicator: 'green',
							message: __('SMS Sent successfully')
						});
					}
				});
			})

			//add send print button
			frm.add_custom_button(__('Send Print'),function(){

				frappe.call({
					'method':'printnode_integration.events.print_via_printnode',
					args:{
						'doctype':frm.doc.doctype,
						'docname':frm.doc.name,
						'docevent':'Submit'
					},
					freeze:true,
				    'freeze_message': __('Sending documents to the printer'),
					callback:function(){
						frappe.msgprint(__('Document Sent to Printer'))
					}
				})

			})
			frm.add_custom_button(__("Download PDF"),()=>{
				//download pdf
				frappe.call({
					method: 'ctc.corona_test_center.doctype.ctc_lab_test.ctc_lab_test.get_lab_test_pdf_link',
					args:{
						
						'doctype':cur_frm.doc.doctype,
						'doc':cur_frm.doc,
						'name':cur_frm.doc.name,
						
					},
					callback:function(message){
						var url = message['message']
						download_file(url,'kask.pdf')
						//window.location.href = message['message']
					}
				})
			})
		}
		
	},
	report_preference:function(frm){
		if (frm.doc.report_preference == 'Print'){
			cur_frm.set_value('print_on_submit',1)
			cur_frm.refresh_field('print_on_submit')
		} else {
			cur_frm.set_value('print_on_submit',0)
			cur_frm.refresh_field('print_on_submit')
		}
	},
	before_save:function(frm){
		console.log('working')
		frappe.call({
			method: 'ctc.app.create_queue',
			args: {
				'ctc_doc':cur_frm.doc
			},
			callback: function (r) {
			}
		});
	},

	// after_workflow_action:function(frm){
	// 	if (frm.doc.workflow_state = 'Submitted'){
	// 		//cur_frm.doc.workflow_state = 'Submitted'
	// 		setTimeout(function(){cur_frm.print_doc() }, 2500);

	// 	}
	// }
	
});


/* Helper function */
function download_file(fileURL, fileName) {
	// for non-IE
	if (!window.ActiveXObject) {
		var save = document.createElement('a');
		save.href = fileURL;
		save.target = '_blank';
		var filename = fileURL.substring(fileURL.lastIndexOf('/')+1);
		save.download = fileName || filename;
		   if ( navigator.userAgent.toLowerCase().match(/(ipad|iphone|safari)/) && navigator.userAgent.search("Chrome") < 0) {
				document.location = save.href; 
	// window event not working here
			}else{
				var evt = new MouseEvent('click', {
					'view': window,
					'bubbles': true,
					'cancelable': false
				});
				save.dispatchEvent(evt);
				(window.URL || window.webkitURL).revokeObjectURL(save.href);
			}   
	}
	
	// for IE < 11
	else if ( !! window.ActiveXObject && document.execCommand)     {
		var _window = window.open(fileURL, '_blank');
		_window.document.close();
		_window.document.execCommand('SaveAs', true, fileName || fileURL)
		_window.close();
	}
}
