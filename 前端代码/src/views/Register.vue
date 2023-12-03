<template>
    <div class="background-container">
        <el-form ref="form" label-width="79px" :inline="true" class="register-container" :model="form" :rules="rules">
            <h3 class="register_title">用户注册</h3>
            <el-form-item label="用户名" prop="username">
                <el-input v-model="form.username" placeholder="请输入账号"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password1">
                <el-input type="password" v-model="form.password1" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="password2">
                <el-input type="password" v-model="form.password2" placeholder="请再次输入密码"></el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="validcode" style="display: flex">
                <el-input v-model="form.validcode" placeholder="请输入验证码"></el-input>
                <Validcode @input="createValidCode" />
            </el-form-item>
            <el-form-item>
                <el-button @click="submit" style="margin-left: 80px;" type="primary" size="mini">注册</el-button>
            </el-form-item>
            <el-form-item>
                <el-button @click="returnLogin" style="margin-left: 40px;" type="primary" size="mini">返回</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>


<script>
import Validcode from '@/components/Validcode.vue';
import { register } from '@/api'
import { checkUsername } from '@/api'

export default {
    components: {
        Validcode
    },
    data() {
        //校验用户名是否存在
        const rulesUsername = (rules, value, callback) => {
            //使用Axios进行校验
            checkUsername(value).then(res => {
                //请求成功
                if (res.data.code === 1) {
                    if (res.data.exist) {
                        callback(new Error("该用户名已存在！"))
                    } else {
                        callback()
                    }
                } else {
                    //请求失败
                    callback("后端校验用户名出现异常！")
                }
            }).catch((err) => {
                console.log(err)
            })
        };
        var validatePass = (rule, value, callback) => {
            if (value === "") {
                callback(new Error("请输入密码"));
            } else {
                if (this.form.password2 !== "") {
                    this.$refs.form.validateField("password2");
                }
                callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            if (value === "") {
                callback(new Error("请再次输入密码"));
            } else if (value !== this.form.password1) {
                callback(new Error("两次输入密码不一致!"));
            } else {
                callback();
            }
        };
        return {
            radio: '',
            form: {
                username: '',
                password1: '',
                password2: '',
                validcode: '',
            },
            rules: {
                username: [
                    { required: true, trigger: 'blur', message: '请输入用户名' },
                    { pattern: /^\w{3,10}$/, message: '由英文数字或下划线组成长度6~10位', trigger: 'blur' },
                    { validator: rulesUsername, trigger: 'blur' },
                ],
                password1: [
                    { required: true, trigger: 'blur', message: '请输入密码' },
                    { validator: validatePass, trigger: 'blur', },
                ],
                password2: [
                    { required: true, trigger: 'blur', message: '请再次输入密码' },
                    { validator: validatePass2, trigger: 'blur', },
                ],
                validcode: [
                    { required: true, trigger: 'blur', message: '请输入验证码' }
                ],
            }
        };
    },
    methods: {
        //生成图形验证码
        createValidCode(data) {
            this.validcode = data
        },
        // 注册
        submit() {
            this.$refs.form.validate((valid) => {
                if (valid) {
                    if (this.form.validcode.toLowerCase() !== this.validcode.toLowerCase()) {
                        this.$message.error("验证码错误")
                        return
                    }
                    let that = this
                    register(that.form.username, that.form.password1,).then(function (res) {
                        //注册成功
                        if (res.data.code === 1) {
                            that.$message({
                                message: '注册成功',
                                type: 'success'
                            })
                            that.$router.push('login');//跳转登录页面
                        }
                        else {
                            //注册失败
                            that.$message.error(res.data.msg)
                        }
                    })
                }
            })
        },
        returnLogin() {
            this.$router.push('login');//跳转登录页面
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

    .register-container {
        width: 400px;
        border: 1px solid #eaeaea;
        margin: 180px auto;
        padding: 35px 35px 1px 35px;
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        box-shadow: 0 0 25px #909399;
        box-sizing: border-box;

        .register_title {
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
