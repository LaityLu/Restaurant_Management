<template>
    <div class="background-container">
        <el-form ref="form" label-width="70px" :inline="true" class="login-container" :model="form" :rules="rules">
            <h3 class="login_title">系统登录</h3>
            <el-form-item label="用户名" prop="username">
                <el-input v-model="form.username" placeholder="请输入账号"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
                <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="validcode" style="display: flex">
                <el-input v-model="form.validcode" placeholder="请输入验证码"></el-input>
                <Validcode @input="createValidCode" />
            </el-form-item>
            <el-radio-group v-model="form.radio" style="margin-left:10% ;">
                <el-radio :label="'0'">店长</el-radio>
                <el-radio :label="'1'">副店长</el-radio>
                <el-radio :label="'2'">管理员</el-radio>
            </el-radio-group>
            <el-form-item>
                <el-button @click="Login" style="margin-left: 50px;margin-top: 30px;" type="primary"
                    size="mini">登录</el-button>
            </el-form-item>
            <el-form-item>
                <el-button @click="register" style="margin-left: 40px;margin-top: 30px;" type="primary"
                    size="mini">注册</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>


<script>

import Cookie from 'js-cookie'
import Validcode from '@/components/Validcode.vue';
import { login } from '@/api'

export default {
    components: {
        Validcode
    },
    data() {
        return {
            form: {
                radio: '',
                username: '',
                password: '',
                validcode: '',
            },
            menuData: [],
            token: '',
            rules: {
                username: [
                    { required: true, trigger: 'blur', message: '请输入用户名' },
                    { pattern: /^\w{3,10}$/, message: '由英文数字或下划线组成长度6~10位', trigger: 'blur' }
                ],
                password: [
                    { required: true, trigger: 'blur', message: '请输入密码' }
                ],
                validcode: [
                    { required: true, trigger: 'blur', message: '请输入验证码' }
                ],
            },
        };
    },
    methods: {
        //生成图形验证码
        createValidCode(data) {
            this.validcode = data
        },
        // 登录
        Login() {
            //表单校验通过
            // console.log(this.form)
            this.$refs.form.validate((valid) => {
                if (valid) {
                    if (this.form.validcode.toLowerCase() !== this.validcode.toLowerCase()) {
                        this.$message.error("验证码错误")
                        return
                    }
                    let that = this
                    login(that.form.username, that.form.password, that.form.radio,).then(function (res) {
                        //请求成功
                        if (res.data.code === 1) {
                            if (that.form.radio === '0') {
                                that.menuData = [
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
                                ]
                            } else if (that.form.radio === '1') {
                                that.menuData = [
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
                                ]
                            } else if (that.form.radio === '2') {
                                that.menuData = [
                                    {
                                        path: '/home',
                                        name: 'home',
                                        label: '首页',
                                        icon: 's-home',
                                        url: 'Home.vue'
                                    },
                                    {
                                        path: '/admin',
                                        name: 'admin',
                                        label: '用户管理',
                                        icon: 's-home',
                                        url: 'Admin.vue'
                                    },
                                ]
                            }
                            // console.log(that.menuData)
                            // 获取左侧菜单的数据，存入store中
                            that.$store.commit('setMenu', that.menuData)
                            that.$store.commit('addMenu', that.$router)
                            that.token = Math.random()
                            // token，radio信息存入cookie用于不同页面间的通信
                            Cookie.set('token', that.token)
                            Cookie.set('radio', that.form.radio)
                            Cookie.set('username', that.form.username)
                            // 跳转到首页
                            that.$router.push('/home')
                        } else {
                            that.$message.error("账号或密码错误! ");
                        }
                    }).catch(function (err) {
                        console.log(err)
                        that.$message.error("获取后端数据出现问题！")
                    })
                }
            })
        },
        register() {
            this.$router.push('register');//跳转注册页面
        },
    }
};
</script>

<style lang="less" scoped>
.background-container {
    background-image: url('../assets/images/background.jpg');
    width: 100%;
    height: 100%;
    position: fixed;
    background-size: 100% 100%;

    .login-container {
        width: 350px;
        border: 1px solid #eaeaea;
        margin: 180px auto;
        padding: 35px 35px 1px 35px;
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        box-shadow: 0 0 25px #909399;
        box-sizing: border-box;

        .login_title {
            text-align: center;
            margin-bottom: 40px;
            color: #505458;
        }

        .el-input {
            width: 198px;
        }
    }
}
</style>
