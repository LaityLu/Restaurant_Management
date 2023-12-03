<!-- header组件 -->
<template>
    <div class="header-container">
        <!-- 包含两个小组件 -->
        <div class="l-content">
            <!-- 导航菜单按钮组件 -->
            <el-button style="margin-right: 20px;" @click="handleMenu" icon="el-icon-menu" size="mini"></el-button>
            <!-- 面包屑组件 -->
            <el-breadcrumb separator=">">
                <el-breadcrumb-item v-for="item in tags" :key="item.path">
                    {{ item.label }}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="r-content">
            <span class="r-content-text">
                你好！{{ username }}
            </span>
            <el-dropdown @command="handleClick" trigger="click">
                <span class="el-dropdown-link">
                    <img class="user" :src="updateImageSource" alt="个人头像" />
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item command="modifyPassword">修改密码</el-dropdown-item>
                    <el-dropdown-item command="logout">退出</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
        <el-dialog title="修改密码" :visible.sync="dialogVisible" class="dialogStyle" :close-on-click-modal="false"
            :before-close="handleClose">
            <el-form ref="form" :rules="rules" class="formStyle" :model="form">
                <el-form-item label="原密码" prop="old_password" :label-width="formLabelWidth">
                    <el-input v-model="form.old_password" type="password" autocomplete="off"
                        suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="新密码" prop="new_password" :label-width="formLabelWidth">
                    <el-input v-model="form.new_password" type="password" autocomplete="off"
                        suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="check_password" :label-width="formLabelWidth">
                    <el-input v-model="form.check_password" type="password" autocomplete="off"
                        suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="submit">确 定</el-button>
                <el-button type="info" @click="cancel">取 消</el-button>
            </div>
        </el-dialog>
    </div>
</template>
<script>

import { mapState } from "vuex";
import Cookie from 'js-cookie'
import img1 from '../assets/images/1.jpg'
import img2 from '../assets/images/2.jpg'
import img3 from '../assets/images/3.jpg'
import { login } from '@/api'
import { modifyPassword } from '@/api'

export default {
    data() {
        //校验原密码是否正确
        const rulesPassword = (rules, value, callback) => {
            this.radio = Cookie.get('radio')
            this.username = Cookie.get('username')
            // console.log(this.username, value, this.radio)
            //使用Axios进行校验
            login(this.username, value, this.radio).then(res => {
                //请求成功
                if (res.data.code === 1) {
                    callback()
                } else if (res.data.code === 2) {
                    callback(new Error("原密码错误！"))
                } else {
                    //请求失败
                    callback("后端校验出现异常！")
                }
            }).catch((err) => {
                console.log(err)
            })
        };
        var validatePass = (rule, value, callback) => {
            if (value === "") {
                callback(new Error("请输入密码"));
            } else {
                if (this.form.check_password !== "") {
                    this.$refs.form.validateField("check_password");
                }
                callback();
            }
        };
        var validatePass2 = (rule, value, callback) => {
            if (value === "") {
                callback(new Error("请再次输入密码"));
            } else if (value !== this.form.new_password) {
                callback(new Error("两次输入密码不一致!"));
            } else {
                callback();
            }
        };
        return {
            username: '',
            radio: '',
            dialogVisible: false,
            form: {
                old_password: '',
                new_password: '',
                check_password: '',
            },
            rules: {
                old_password: [
                    { required: true, message: "请输入原密码", trigger: 'blur', },
                    { validator: rulesPassword, trigger: 'blur' },
                ],
                new_password: [
                    { required: true, trigger: 'blur', message: '请输入新密码' },
                    { validator: validatePass, trigger: 'blur', },
                ],
                check_password: [
                    { required: true, trigger: 'blur', message: '请再次输入密码' },
                    { validator: validatePass2, trigger: 'blur', },
                ],

            },
            formLabelWidth: '120px'
        };
    },
    methods: {
        //展开或关闭左侧导航栏
        handleMenu() {
            this.$store.commit('collapseMenu')
        },
        //实现注销和修改密码功能
        handleClick(command) {
            if (command === 'logout') {
                this.$confirm('是否确认退出登录?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                    center: true
                }).then(() => {
                    this.$message({
                        type: 'success',
                        message: '成功退出!'
                    });
                    //清除token的数据
                    Cookie.remove('token')
                    //清除menuData的数据
                    Cookie.remove('menuData')
                    //清除radio的数据
                    Cookie.remove('radio')
                    Cookie.remove('username')
                    //跳转到登录页面
                    this.$router.push('/login')
                }).catch(() => { });
            }
            else if (command === 'modifyPassword') {
                this.dialogVisible = true
            }
        },
        //点击确定，提交表单
        submit() {
            this.$refs.form.validate((valid) => {
                const formData = { ...this.form };
                if (valid) {
                    //校验成功后，执行修改
                    let that = this
                    modifyPassword(that.username, that.form.new_password).then(res => {
                        //执行成功
                        if (res.data.code === 1) {
                            that.$message({
                                message: '修改成功',
                                type: 'success'
                            })
                        }
                        else {
                            //请求失败
                            that.$message.error(res.data.msg)
                        }
                    }).catch(err => {
                        //执行失败
                        console.log(err)
                        that.$message.error("后端修改数据出现问题！")
                    })
                    //关闭弹窗
                    this.handleClose()
                } else {
                    //校验失败
                    console.log("error submit!")
                    return false
                }
            })
        },
        //弹窗关闭的时候触发
        handleClose() {
            //清除表单中的信息
            this.form = {}
            //清除表单的校验
            this.$refs.form.resetFields()
            this.dialogVisible = false
        },
        //点击取消
        cancel() {
            this.handleClose()
        },
    },
    computed: {
        //利用辅助函数获取state中的tabsList
        ...mapState({
            tags: (state) => state.tab.tabsList,
            currentMenu: (state) => state.tab.currentMenu,
        }),
        updateImageSource() {
            this.username = Cookie.get('username')
            const radio = String(Cookie.get('radio'))
            if (radio === '1') {
                return img1;//副店长
            } else if (radio === '0') {
                return img2;//店长
            } else if (radio === '2') {
                return img3;//管理员
            }
        }
    },
};
</script>
<style lang="less" scoped>
.header-container {
    padding: 0 20px;
    background-color: #333;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .dialogStyle {
        width: 100%,
    }

    .formStyle {
        padding-left: 10%;
        width: 70%,
    }

    //右侧图标样式
    .r-content {
        display: flex;
        align-items: center;

        .user {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            margin-left: 20px;
        }

        .r-content-text {
            color: #FFFFFF;
            font-family: "微软雅黑";
            line-height: 1.5;
            font-size: 110%;
        }
    }

    //优化面包屑的样式
    .l-content {
        display: flex;
        align-items: center;

        /deep/.el-breadcrumb__item {
            .el-breadcrumb__inner {
                font-weight: normal;

                &.is-link {
                    color: #666;
                }
            }

            //找到最后一个子元素，即最后选中的面包屑标签
            &:last-child {
                .el-breadcrumb__inner {
                    color: #fff;
                }
            }
        }
    }
}
</style>