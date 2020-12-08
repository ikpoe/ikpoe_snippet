Metabase bulk update email
--
This script is used for email domain migration. It will update email that is used for login to a new domain.

Requirements
---
This script is tested in Python 3.9.0

Need to set some this variable:
- metabase_url = [METABASE_URL]
- email = [ADMIN_EMAIL]
- password = [ADMIN_PASSWORD]
- filename = "list_users_email.csv"
- email_domain = [NEW_EMAIL_DOMAIN]
