from django.test import TestCase
from appSite.models import Worker
from datetime import date
import openpyxl

# Create your tests here.

class WorkerTests(TestCase):
    def setUp(self):
        print('setUp')
        for i in range(5):
            Worker.objects.create(
                W_id=i+10,
                W_name='stu1',
                W_sex=1,  # 1表示男性
                W_birth=date(1990+i, 5, 15),  # 出生日期
                W_job=0,  # 0表示服务员
                W_phone="1234567890",  # 电话号码
                W_salary=2500,  # 工资
                W_addr="123 Main St"  # 家庭住址
            )

    def test_get_worker_age(self):
        obj_worker = Worker.objects.all().values()
        worker_list = []
        for worker in obj_worker:
            today = date.today()
            age = today.year - worker['W_birth'].year - (
                        (today.month, today.day) < (worker['W_birth'].month, worker['W_birth'].day))
            worker['W_age'] = age
            # worker_info = {
            #     "age": age
            # }
            # print(age)
            worker_list.append(worker)
        print(worker_list)
        self.assertTrue(True)  # 用合适的断言来验证测试结果

