import requests

class Metabase_API():
  
  def __init__(self, domain, email, password):
    
    self.domain = domain
    self.email = email
    self.password = password
    self._header = None
    self.authenticate()
    self._users = None
  
  @property
  def header(self):
    if self._header == None:
      self._header = self.authenticate()
    return self._header
  
  @property
  def users(self):
    if self._users == None:
      self._users = self.get(f"/api/user")
    return self._users
  
  def authenticate(self):
    """Get a Session ID"""
    conn_header = {'username':self.email,
                   'password':self.password}

    res = requests.post(self.domain + '/api/session', json = conn_header)
    if not res.ok:
      raise Exception(res)
    
    session_id = res.json()['id']
    return {'X-Metabase-Session':session_id}
  
  
  def validate_session(self):
    """Get a new session ID if the previous one has expired"""
    res = requests.get(self.domain + '/api/user/current', headers = self.header)
    
    if res.ok:  # 200
      return True
    elif res.status_code == 401:  # unauthorized
      return self.authenticate()
    else:
      raise Exception(res)
  
  
  
  ######################### REST Methods ###########################
  
  def get(self, endpoint, **kwargs):
    res = requests.get(self.domain + endpoint, headers=self.header, **kwargs)
    return res.json() if res.ok else False
  
  
  # def post(self, endpoint, **kwargs):
  #   res = requests.post(self.domain + endpoint, headers=self.header, **kwargs)
  #   return res.json() if res.ok else False
  
  
  def put(self, endpoint, **kwargs):
    """Used for updating objects"""
    res = requests.put(self.domain + endpoint, headers=self.header, **kwargs)
    return res.status_code
  
  
  # def delete(self, endpoint, **kwargs):
  #   res = requests.delete(self.domain + endpoint, headers=self.header, **kwargs)
  #   return res.status_code
    
  def get_user(self, user_id):
    res = self.get(f"/api/user/{user_id}")
    if res:
      return res
    else:
      raise ValueError(f"There is no user with the id {user_id}")
  
  ###############
  
  def get_user_by_email(self, email):
    list_users = [ user for user in self.users if user['email'] == email ]
    
    if len(list_users) > 1:
      raise ValueError(f"There is more than one user with the name '{email}'")

    if len(list_users) == 0:
      raise ValueError(f"There is no user with the name '{email}'")
    
    return list_users[0]
  
  def get_all_users(self):
    return self.get(f"/api/user")
  
  
  def update_email_domain(self, user, domain):
    
    username = user['email'].split("@")[0]
    new_email = username + "@" + domain
    
    self.put(f"/api/user/{user['id']}", json = {'email': new_email} )
  
  
##################################################################

def main():
  metabase_url = [METABASE_URL]
  email = [ADMIN_EMAIL]
  password = [ADMIN_PASSWORD]
  filename = "list_users_email.csv"
  email_domain = [NEW_EMAIL_DOMAIN]

  migrated_users = open(filename).read().splitlines()
  mi = Metabase_API(metabase_url,email,password)

  successful_users = []
  failed_users = []
  for mi_user in migrated_users:
    migrated_email = mi_user # need to change if the list is username only (without domain)
    try:
      user_data = mi.get_user_by_email(migrated_email)
      mi.update_email_domain(user_data, email_domain)
      successful_users.append(migrated_email)
    except:
      failed_users.append(migrated_email)

  print(f"Successful Migrated User: {successful_users}")
  print(f"Failed Migrated User: {failed_users}")

if __name__ == "__main__":
    main()
