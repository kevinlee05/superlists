from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://klee05.pythonanywhere.com')

assert 'Django' in browser.title 


