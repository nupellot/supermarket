select user_id, user_group
from internal_user
where user_login = "$login" and user_password ="$password"
