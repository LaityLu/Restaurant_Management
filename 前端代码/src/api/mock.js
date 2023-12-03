import Mock from 'mockjs'
import customerApi from "./mockServeData/customer"
import workerApi from "./mockServeData/worker"
import dishApi from "./mockServeData/dish"
import permission from './mockServeData/permission'


// 定义mock请求拦截
//获得菜单数据
// Mock.mock('/api/menu/getDish', dishApi.getDishList)
//获得顾客数据
// Mock.mock('/api/customer/getCustomer', customerApi.getCustomerList)
//获得员工数据
// Mock.mock('/api/worker/getWorker', workerApi.getWorkerList)
//获得登录数据
// Mock.mock(/api\/permission\/getMenu/, 'post', permission.getMenu)