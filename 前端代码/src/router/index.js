import Vue from "vue";
import VueRouter from "vue-router";
import Main from "../views/Main.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Admin from "../views/Admin.vue";



Vue.use(VueRouter);

//1.创建路由组件
//2.将路由与组件进行映射
//3.创建 router 实例，然后传 `routes` 配置
//4.创建和挂载根实例。

const routes = [
  {
    //主路由 1
    path: "/",
    component: Main,
    name:'Main',
    redirect:'/home',
    children: [
      //子路由
      // { path: "/home",name: 'home', component: Home },//首页
      // { path: "/menu", name: 'menu',component: Menu },//菜单管理
      // { path: "/foodtable", name: 'foodtable',component: FoodTable },//菜单管理
      // { path: "/customer",name: 'customer', component: Customer },//顾客管理
      // { path: "/worker", name: 'worker',component: Worker },//员工管理
      // { path: "/orderone",name: 'orderone', component: OrderOne },//已完成订单管理
      // { path: "/ordertwo", name: 'ordertwo',component: OrderTwo },//未完成订单管理
      // 当 / 匹配成功，
      // Home、User 会被渲染在 Main的 <router-view> 中
      // {
      //   path: 'posts',
      //   component: UserPosts
      // }
    ],
  },
  {
    //主路由 2
    path: "/login",
    component: Login,
    name: 'login',
  },
  {
    //主路由 3
    path: "/register",
    component: Register,
    name: 'register',
  },
  // {
  //   //主路由 4
  //   path: "/admin",
  //   component: Admin,
  //   name: 'admin',
  // },
];

const router = new VueRouter({
  routes, // (缩写) 相当于 routes: routes
});

export default router;
