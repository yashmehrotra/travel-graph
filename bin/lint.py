import soldier
a = soldier.run('flake8 .')
if a.status_code != 0:
    print a.output[:-1]
else:
    print 'Ready to go, good job following pep8'
