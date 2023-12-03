<template>
    <div style="padding-left:60px">
        <el-form :inline="true">
            <el-form-item>
                <el-input placeholder="请输入查询条件" v-model="inputstr" :clearable="true">
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="queryCustomerData()" icon="el-icon-search" plain size="medium">
                    查询
                </el-button>
                <el-button type="primary" @click="getALLCustomerData()" icon="el-icon-tickets" plain size="medium">
                    全部
                </el-button>
                <el-button @click="handelExportToExcel()" type="primary" icon="el-icon-download" style="margin-bottom: 14px"
                    plain size="medium" :disabled="isButtonDisabled">导出Excel
                </el-button>
            </el-form-item>
        </el-form>
        <el-table :data="pagetable" :border="true" style="width: 70%" stripe>
            <el-table-column prop="C_account" label="账号" width="180">
            </el-table-column>
            <el-table-column prop="C_name" label="姓名" width="180">
            </el-table-column>
            <el-table-column prop="C_sex" label="性别" width="180">
                <template slot-scope="scope">
                    <span>{{ scope.row.C_sex }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="C_phone" label="电话" width="180">
            </el-table-column>
            <el-table-column prop="C_ordernum" label="完成订单数">
            </el-table-column>
        </el-table>
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
<script>

import { getCustomer } from '@/api';
import { queryCustomer } from '@/api';
import { exportToExcel } from '@/api'
import Cookie from 'js-cookie';
export default {
    data() {
        return {
            form: {
                C_account: '',
                C_name: '',
                C_sex: '',
                C_phone: '',
                C_ordernum: '',
            },
            total: 0,//数据总行数
            currentpage: 1,//当前页码
            pagesize: 8,//每页行数
            pagetable: [],//分页后当前页的数据
            tableData: [],//全部顾客信息
            inputstr: '',//接收查询条件
            raido: ''
        };
    },
    methods: {
        //获取顾客信息
        getCustomerData: function () {
            let that = this//axios执行异步请求后,会让 this指向undefine
            getCustomer().then(function (res) {
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
                that.$message.error("获取取后端数据出现问题！")
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
        getALLCustomerData() {
            //清空查询条件
            this.inputstr = ''
            //获取全部数据
            this.getCustomerData()
        },
        //查询顾客信息
        queryCustomerData() {
            if (this.inputstr === '') {
                this.$message({
                    message: '查询条件不能为空！',
                    type: 'warning'
                });
                return
            }
            //使用Ajax请求---post---传递inputstr
            let that = this
            queryCustomer(that.inputstr).then(function (res) {
                //请求成功
                if (res.data.code === 1) {
                    that.tableData = res.data.data
                    //获取当前返回记录的总行数
                    that.total = res.data.data.length
                    //获取当前页的数据
                    that.getPageData()
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
            exportToExcel("Customer").then(res => {
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
        this.getCustomerData();
    },
    computed: {
        //控制按钮是否禁用
        isButtonDisabled() {
            this.radio = Cookie.get('radio')
            return this.radio === '0' ? false : true;
        },
    },
};
</script>