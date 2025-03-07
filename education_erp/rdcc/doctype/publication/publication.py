import frappe
from frappe.model.document import Document
import re
from frappe import _

class Publication(Document):
    @frappe.whitelist()
    def validate(self):
        # Validate and format the title
        if self.get("title"):
            self.set("title", str(self.get("title")).upper())


    @frappe.whitelist()
    def on_submit(self, new_status="Pending"):
        self.status = new_status
        self.save()

    @frappe.whitelist()
    def approve(self):
        self.status = "Approved"
        self.save()

    @frappe.whitelist()
    def reject(self):
        self.status = "Rejected"
        self.save()

    # @frappe.whitelist()
    # def cancel(self):
    #     self.status = "Cancelled"
    #     self.save()

# my_custom_app/notifications.py
@frappe.whitelist()
def notify_users(users, message, subject):
    print("Users to notify:", users)
    for user in users:
        print("Sending notification to:", user)
        frappe.publish_realtime(event='notification', message={
            'message': message,
            'subject': subject,
            'user': user
        }, user=user)
    return "Notifications sent successfully."

@frappe.whitelist()
def get_instructor_program_details():
    current_user = frappe.session.user
    query = """
        SELECT
            i.employee,
            i.custom_user_id,
            i.custom_program,
            p.custom_head_of_department_user_id,
            p.custom_portfolio_coordinator_user_id
        FROM
            `tabInstructor` i
        JOIN
            `tabProgram` p
        ON
            i.custom_program = p.program_name
        WHERE
            i.custom_user_id = %s;
    """
    results = frappe.db.sql(query, current_user, as_dict=True)
    return results