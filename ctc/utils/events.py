import frappe

@frappe.whitelist()
def get_events(start,end,filters=None):

    # res=frappe.db.sql(f"""select name ,
    #             appointment as start, appointment_end as end
    #     from `tabCTC Lab Test` where docstatus =1  and appointment is not null and appointment_end is not null
    #      and date(appointment) BETWEEN date('{start}') and date('{end}')""",as_dict=1)
    # r=res
    filters={'docstatus':1,'appointment_end':['is','set']}
    res = frappe.get_all("CTC Lab Test",fields=['appointment','appointment_end','name','full_name'], filters=filters)
    return res
        