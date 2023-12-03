<template>
    <div style="padding-left:60px">
        <!-- 提示窗 -->
        <el-dialog :title="dialogTitle" :before-close="handleClose" :visible.sync="dialogVisible" width="50%"
            :close-on-click-modal="false">
            <!-- 员工表单信息 -->
            <el-form ref="form" :rules="rules" :inline="true" :model="form" label-width="80px" label-position="right">
                <el-form-item label="工号" prop="W_id">
                    <el-input placeholder="请输入工号" :disabled="isEdit" v-model="form.W_id"
                        suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="姓名" prop="W_name">
                    <el-input placeholder="请输入姓名" v-model="form.W_name" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="性别" prop="W_sex">
                    <el-select v-model="form.W_sex" placeholder="请选择性别">
                        <el-option label="男" value='男'></el-option>
                        <el-option label="女" value='女'></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="出生日期" prop="W_birth">
                    <el-date-picker type="date" placeholder="选择日期" v-model="form.W_birth" value-format="yyyy-MM-dd">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="家庭住址" prop="W_addr">
                    <el-input placeholder="请输入地址" v-model="form.W_addr" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="电话" prop="W_phone">
                    <el-input placeholder="请输入电话" v-model="form.W_phone" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="职务" prop="W_job">
                    <el-select placeholder="请选择职务" v-model="form.W_job">
                        <el-option label="厨师" value="厨师"></el-option>
                        <el-option label="服务员" value="服务员"></el-option>
                        <el-option label="保洁" value="保洁"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="工资" prop="W_salary">
                    <el-input placeholder="请输入工资" v-model="form.W_salary" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="submit">确 定</el-button>
                <el-button type="info" @click="cancel">取 消</el-button>
            </span>
        </el-dialog>
        <div class=functionstyle>
            <!-- 新增按钮 -->
            <el-button @click="addform()" type="primary" icon="el-icon-circle-plus-outline" style="margin-bottom: 14px"
                plain size="medium" :disabled="isButtonDisabled">新增
            </el-button>
            <el-button @click="handelExportToExcel()" type="primary" icon="el-icon-download" style="margin-bottom: 14px"
                plain size="medium" :disabled="isButtonDisabled">导出Excel
            </el-button>
            <el-form :inline="true" style="margin-left: 320px ">
                <el-form-item>
                    <el-input v-model="inputstr" placeholder="请输入查询条件" :clearable="true">
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="queryWorkerData()" icon="el-icon-search" plain size="medium">
                        查询
                    </el-button>
                    <el-button type="primary" @click="getALLWorkerData()" icon="el-icon-tickets" plain size="medium">
                        全部
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
        <div>
            <el-table :data="pagetable" :border="true" style="width: 90%" stripe>
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <el-form label-position="left" inline class="demo-table-expand">
                            <el-form-item label="工号:">
                                <span>{{ props.row.W_id }}</span>
                            </el-form-item>
                            <el-form-item label="姓名:">
                                <span>{{ props.row.W_name }}</span>
                            </el-form-item>
                            <el-form-item label="性别:">
                                <span>{{ props.row.W_sex }}</span>
                            </el-form-item>
                            <el-form-item label="年龄:">
                                <span>{{ props.row.W_age }}</span>
                            </el-form-item>
                            <el-form-item label="职务:">
                                <span>{{ props.row.W_job }}</span>
                            </el-form-item>
                            <el-form-item label="工资:">
                                <span>{{ props.row.W_salary }}</span>
                            </el-form-item>
                            <el-form-item label="出生日期:">
                                <span>{{ props.row.W_birth }}</span>
                            </el-form-item>
                            <el-form-item label="家庭住址:">
                                <span>{{ props.row.W_addr }}</span>
                            </el-form-item>
                            <el-form-item label="电话号码:">
                                <span>{{ props.row.W_phone }}</span>
                            </el-form-item>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column label="工号" prop="W_id" width='180'>
                </el-table-column>
                <el-table-column label="姓名" prop="W_name" width='180'>
                </el-table-column>
                <el-table-column label="性别" prop="W_sex" width='180'>
                    <template slot-scope="scope">
                        <span>{{ scope.row.W_sex }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="年龄" prop="W_age" width='180'>
                    <template slot-scope="scope">
                        <span>{{ scope.row.W_age }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="职务" prop="W_job" width='180'>
                    <template slot-scope="scope">
                        <span>{{ scope.row.W_job }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button type="success" size="mini" icon="el-icon-edit" @click="updateform(scope.row)"
                            :disabled="isButtonDisabled"></el-button>
                        <el-button type="danger" size="mini" icon="el-icon-delete" @click="deleteWorkerData(scope.row)"
                            :disabled="isButtonDisabled"></el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <!-- 分页 -->
        <el-row style="margin-top: 10px; padding-right: 20px;">
            <el-col style="text-align: right;">
                <el-pagination @current-change="handleCurrentChange" :current-page.sync="currentpage" :page-size="pagesize"
                    layout="total, prev, pager, next, jumper" :total="total">
                </el-pagination>
            </el-col>
        </el-row>
    </div>
</template>

<style lang="less" scoped>
.demo-table-expand {
    font-size: 0;
}

.demo-table-expand label {
    width: 90px;
    color: #99a9bf;
}

.demo-table-expand .el-form-item {
    padding-left: 50px;
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
}

.functionstyle {
    display: flex;
    align-items: center;
}
</style>

<script>
import { getWorker } from '@/api'
import { queryWorker } from '@/api'
import { checkWid } from '@/api'
import { addWorker } from '@/api'
import { updateWorker } from '@/api'
import { deleteWorker } from '@/api'
import { exportToExcel } from '@/api'
import Cookie from 'js-cookie';

export default {
    data() {
        //校验工号是否存在
        const rulesW_id = (rules, value, callback) => {
            if (this.isEdit) {
                callback()
            }
            //使用Axios进行校验
            checkWid(value).then(res => {
                //请求成功
                if (res.data.code === 1) {
                    if (res.data.exist) {
                        callback(new Error("工号已存在！"))
                    } else {
                        callback()
                    }
                } else {
                    //请求失败
                    callback("后端校验工号出现异常！")
                }
            }).catch((err) => {
                console.log(err)
            })
        }
        return {
            dialogVisible: false,
            dialogTitle: '',
            isEdit: false,//标识是否是修改
            form: {
                W_id: '',
                W_name: '',
                W_sex: '',
                W_age: '',
                W_birth: '',
                W_addr: '',
                W_phone: '',
                W_job: '',
                W_salary: '',
            },
            rules: {
                W_id: [
                    { required: true, message: "请输入工号", trigger: 'blur', },
                    { pattern: /^[6][5]\d{3}$/, message: "必须是以\"65\"开头的五位数", trigger: 'blur' },
                    { validator: rulesW_id, trigger: 'blur' },
                ],
                W_name: [
                    { required: true, message: "请输入姓名", trigger: 'blur', },
                    { pattern: /^[\u4e00-\u9fa5]{2,5}$/, message: "必须是2~5个汉字", trigger: 'blur' },
                ],
                W_sex: [{
                    required: true, message: "请输入性别", trigger: 'change',
                }],
                W_birth: [{
                    required: true, message: "请输入出生日期", trigger: 'change',
                }],
                W_addr: [{
                    required: true, message: "请输入家庭住址", trigger: 'blur',
                }],
                W_phone: [
                    { required: true, message: "请输入工号", trigger: 'blur', },
                    { pattern: /^[1][35789]\d{9}$/, message: "电话号码必须符合规范", trigger: 'blur' }
                ],
                W_job: [{
                    required: true, message: "请输入职务", trigger: 'change',
                }],
                W_salary: [
                    { required: true, message: "请输入工资", trigger: 'blur', },
                    { pattern: /^\d+$/, message: "必须是数字", trigger: 'blur' },]
            },
            total: 0,//数据总行数
            currentpage: 1,//当前页码
            pagesize: 8,//每页行数
            pagetable: [],//分页后当前页的数据
            tableData: [],//员工表格数据
            inputstr: '',//接收查询条件
            radio: '',
        };
    },
    methods: {
        //弹出表单
        //"添加员工"表单
        addform() {
            //修改标题
            this.dialogTitle = "添加员工信息"
            //弹出表单
            this.dialogVisible = true
        },
        //"修改员工"表单
        updateform(row) {
            //修改标题
            this.dialogTitle = "修改员工信息"
            //标识修改
            this.isEdit = true
            //深拷贝
            this.form = JSON.parse(JSON.stringify(row))
            this.dialogVisible = true
        },
        //点击确定，提交表单
        submit() {
            this.$refs.form.validate((valid) => {
                //console.log(valid,'valid')
                const formData = { ...this.form };
                if (valid) {
                    //校验成功后，执行添加或修改
                    if (this.isEdit) {
                        //修改
                        this.updateWorkerData()
                    }
                    else {
                        //添加
                        this.addWorkerData(formData)
                    }
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
            this.isEdit = false
        },
        //点击取消
        cancel() {
            this.handleClose()
        },
        //添加员工信息
        addWorkerData(formData) {
            let that = this
            addWorker(formData).then(res => {
                //执行成功
                if (res.data.code === 1) {
                    //获取所有员工信息
                    that.tableData = res.data.data
                    //获取当前返回记录的总行数
                    that.total = res.data.data.length
                    //获取当前页的数据
                    that.getPageData()
                    //获取记录条数
                    that.$message({
                        message: '添加成功',
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
                that.$message.error("后端插入数据出现问题！")
            })
        },
        //实现修改功能
        updateWorkerData() {
            let that = this
            updateWorker(that.form).then(res => {
                //执行成功
                if (res.data.code === 1) {
                    //获取所有员工信息
                    that.tableData = res.data.data
                    //获取当前返回记录的总行数
                    that.total = res.data.data.length
                    //获取当前页的数据
                    that.getPageData()
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
        },
        //实现删除功能
        deleteWorkerData(row) {
            this.$confirm('是否确认删除该员工【工号: ' + row.W_id + '\t姓名: ' + row.W_name + '】的信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                //确认删除
                let that = this
                deleteWorker(row.W_id).then(res => {
                    //执行成功
                    if (res.data.code === 1) {
                        //获取所有员工信息
                        that.tableData = res.data.data
                        //获取当前返回记录的总行数
                        that.total = res.data.data.length
                        //获取当前页的数据
                        that.getPageData()
                        that.$message({
                            message: '删除成功!',
                            type: 'success'
                        })
                    }
                    else {
                        //请求失败
                        that.$message.error(res.data.msg)
                    }
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },
        //获取员工信息
        getWorkerData: function () {
            let that = this//axios执行异步请求后,会让 this指向undefine
            getWorker().then(function (res) {
                //请求成功
                if (res.data.code === 1) {
                    that.tableData = res.data.data
                    //获取当前返回记录的总行数
                    that.total = res.data.data.length
                    //获取当前页的数据
                    that.getPageData()
                    // console.log(that.tableData)
                    //提示
                    // that.$message({
                    //     message: '数据加载成功',
                    //     type: 'success'
                    // })
                }
                else {
                    //请求失败
                    that.$message.error(res.data.msg)
                }
            }).catch(function (err) {
                console.log(err)
                that.$message.error("获取后端数据出现问题！")
            })
        },
        //获取当前页数据
        getPageData() {
            //清空pagetable的数据
            this.pagetable = []
            //获取当前页的数据
            for (let i = (this.currentpage - 1) * this.pagesize; i < this.total; i++) {
                //遍历数据添加到pagetable
                this.pagetable.push(this.tableData[i])
                //判断是否达到一页的要求
                if (this.pagetable.length === this.pagesize) break
            }
        },
        //修改当前的页码
        handleCurrentChange(pageNum) {
            //修改页码
            this.currentpage = pageNum
            //重新分页
            this.getPageData()
        },
        //实现"全部"按钮功能
        getALLWorkerData() {
            //清空查询条件
            this.inputstr = ''
            //获取全部数据
            this.getWorkerData()
        },
        //查询员工信息
        queryWorkerData() {
            if (this.inputstr === '') {
                this.$message({
                    message: '查询条件不能为空！',
                    type: 'warning'
                });
                return
            }
            //使用Ajax请求---post---传递inputstr
            let that = this
            console.log(that.inputstr)
            queryWorker(that.inputstr).then(function (res) {
                //请求成功
                if (res.data.code === 1) {
                    that.tableData = res.data.data
                    //获取当前返回记录的总行数
                    that.total = res.data.data.length
                    //获取当前页的数据
                    that.getPageData()
                    // console.log(that.tableData)
                    //提示
                    that.$message({
                        message: '查询成功',
                        type: 'success'
                    })
                }
                else {
                    //查询失败
                    that.$message.error(res.data.msg)
                }
            }).catch(function (err) {
                console.log(err)
                that.$message.error("获取后端查询结果出现问题！")
            })
        },
        //导出到Excel
        handelExportToExcel() {
            let that = this
            exportToExcel("Worker").then(res => {
                //执行成功
                if (res.data.code === 1) {
                    let url = 'http://127.0.0.1:8000/' + 'media/' + res.data.name;
                    // console.log(url)
                    window.open(url)
                    that.$message({
                        message: '下载成功',
                        type: 'success'
                    })
                }
                else {
                    //请求失败
                    that.$message.error("导出到Excel出现异常!")
                }
            }).catch(err => {
                //执行失败
                console.log(err)
            })
        },
    },
    mounted() {
        this.getWorkerData();
    },
    computed: {
        //控制按钮是否禁用
        isButtonDisabled() {
            this.radio = Cookie.get('radio')
            return this.radio === '0' ? false : true;
        },
    }
};
</script>