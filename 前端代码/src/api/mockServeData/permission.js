import Mock from 'mockjs'
import { login } from '@/api'
export default {
  getMenu: config => {
    const { radio, username, password } = JSON.parse(config.body)
    // 先判断用户是否存在
    // 判断账号和密码是否对应
    if (username === 'admin' && password === 'admin'&& (radio === '0'|| radio === '1')) {
      return {
        code: 20000,
        data: {
          menuData: [
             {
                    path: '/home',
                    name: 'home',
                    label: '首页',
                    icon: 's-home',
                    url: 'Home.vue'
                },
                {
                    path: '/menu',
                    name: 'menu',
                    label: '菜单管理',
                    icon: 'food',
                    url: 'Menu.vue'
                },
                {
                    path: '/foodtable',
                    name: 'foodtable',
                    label: '餐桌管理',
                    icon: 's-help',
                    url: 'FoodTable.vue'
                },
                {
                    path: '/customer',
                    name: 'customer',
                    label: '顾客管理',
                    icon: 's-custom',
                    url: 'Customer.vue'
                },
                {
                    path: '/worker',
                    name: 'worker',
                    label: '员工管理',
                    icon: 'user-solid',
                    url: 'Worker.vue'
                },
                {
                    label: '订单管理',
                    icon: 's-order',
                    children: [
                        {
                            path: '/orderone',
                            name: 'orderone',
                            label: '未完成订单',
                            icon: 'error',
                            url: 'OrderOne.vue'
                        },
                        {
                            path: '/ordertwo',
                            name: 'ordertwo',
                            label: '已完成订单',
                            icon: 'success',
                            url: 'OrderTwo.vue'
                        },
                    ],
                },
          ],
          token: Mock.Random.guid(),
          radio: radio,
          message: '获取成功'
        }
      }
    } else if (username === 'xiaoxiao' && password === 'xiaoxiao'&& radio === '2') {
      return {
        code: 20000,
        data: {
          menuData: [
            {
              path: '/custhome',
              name: 'custhome',
              label: '首页',
              icon: 's-home',
              url: 'CustHome.vue'
            },
            {
              path: '/orderdish',
              name: 'orderdish',
              label: '点餐',
              icon: 'food',
              url: 'OrderDish.vue'
            },
            {
                    label: '我的订单',
                    icon: 's-order',
                    children: [
                        {
                            path: '/myorderone',
                            name: 'myorderone',
                            label: '进行中订单',
                            icon: 's-help',
                            url: 'MyOrderOne.vue'
                        },
                        {
                            path: '/myordertwo',
                            name: 'myordertwo',
                            label: '历史订单',
                            icon: 'success',
                            url: 'MyOrderTwo.vue'
                        },
                    ],
                },
          ],
          token: Mock.Random.guid(),
          radio: radio,
          message: '获取成功'
        }
      }
    } else {
      return {
        code: -999,
        data: {
          message: '密码错误'
        }
      }
    }

  }
}