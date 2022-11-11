select user_id, NULL as user_group
from external_user
where user_login = "$login" and user_password = "$password"