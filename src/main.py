import Login
import CVPassComfirm
import asyncio
import TestBasicFunctions
import CatchAndAnalyze

from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


test_catch_html = False
test_sync_flag = False
test_login_flag = False


if __name__ == '__main__':
    
    
    if test_sync_flag:
        print("========================================")
        print("Testing the basic playwright functions:")
        print("========================================")
        TestBasicFunctions.test_sync()
        print("Test finished!")
        #asyncio.run(test_async())
    if test_login_flag:
        print("========================================")
        print("Testing the CVPassConfirm functions:")
        print("========================================")
        Login.LogInWebsite()
        print("Test finished!")
    if test_catch_html:
        print("========================================")
        print("Testing the CVPassConfirm functions:")
        print("========================================")
        CatchAndAnalyze.CatshAndAnalyze()
        print("Test finished!")