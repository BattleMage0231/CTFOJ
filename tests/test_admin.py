def test_admin(client, database):
    '''Test that non-admins are barred from admin pages, and admins can access them.'''
    # Admins should be able to view the page
    database.execute("INSERT INTO 'users' VALUES(1, 'admin', 'pbkdf2:sha256:150000$XoLKRd3I$2dbdacb6a37de2168298e419c6c54e768d242aee475aadf1fa9e6c30aa02997f', 'e', datetime('now'), 1, 0, 1);")
    client.post('/login', data = {'username': 'admin', 'password': 'CTFOJadmin'})
    result = client.get('/admin/users')
    assert result.status_code == 200
    assert b'Users' in result.data
    client.get('/logout')

    # Normal users should be redirected to home
    database.execute("INSERT INTO 'users' VALUES(2, 'normal_user', 'pbkdf2:sha256:150000$XoLKRd3I$2dbdacb6a37de2168298e419c6c54e768d242aee475aadf1fa9e6c30aa02997f', 'e', datetime('now'), 0, 0, 1);")
    result_user = client.post('/login', data = {'username': 'normal_user', 'password': 'CTFOJadmin'}, follow_redirects = True)
    print(result_user.data)
    assert b'Welcome' in result_user.data
    result_user = client.get('/admin/users')
    assert result_user.status_code == 302
    client.get('/logout')
    
    # Not logged in users should be redirected to the login page
    result_nouser = client.get('/admin/users')
    assert result_nouser.status_code == 302
    result_nouser = client.get('/admin/users', follow_redirects=True)
    assert b'Log In' in result_nouser.data
