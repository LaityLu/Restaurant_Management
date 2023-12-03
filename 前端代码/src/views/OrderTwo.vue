<template>
    <div style="padding-left:60px">
        <div class=functionstyle>
            <el-form :inline="true">
                <el-form-item>
                    <el-input v-model="inputstr" placeholder="请输入订单号或账户" :clearable="true">
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="queryOrderData()" icon="el-icon-search" plain size="medium">
                        查询
                    </el-button>
                    <el-button type="primary" @click="getALLOrderData()" icon="el-icon-tickets" plain size="medium">
                        全部
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
        <div>
            <el-table :data="pagetable" :border="true" stripe style="width: 80%">
                <el-table-column prop="O_id" label="订单号" width="180">
                </el-table-column>
                <el-table-column prop="C_account_id" label="顾客账户" width="180">
                </el-table-column>
                <el-table-column prop="O_time" label="时间" width="180">
                </el-table-column>
                <el-table-column prop="Ft_id_id" label="餐桌号" width="180">
                </el-table-column>
                <el-table-column prop="O_cost" label="总金额" width="180">
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button type="info" size="mini" icon="el-icon-more" circle @click="open_detail(scope.row)">
                        </el-button>
                        <el-dialog title="订单详情" :visible.sync="dialogTableVisible">
                            <el-table :data="dishData" :border="true" stripe>
                                <el-table-column property="M_name" label="菜品名称"></el-table-column>
                                <el-table-column property="M_num" label="数量"></el-table-column>
                                <el-table-column property="M_cost" label="价格"></el-table-column>
                            </el-table>
                        </el-dialog>
                        <el-button type="danger" size="mini" icon="el-icon-delete" circle
                            @click="deleteOrderData(scope.row)" style="margin-left: 5px;" :disabled="isButtonDisabled">
                        </el-button>
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

import { getOrder } from '@/api';
import { getOrderDetail } from '@/api';
import { queryOrder } from '@/api';
import { deleteOrder } from '@/api';
import Cookie from 'js-cookie';

export default {
    data() {
        return {
            dialogVisible: false,
            dialogTableVisible: false,
            dialogTitle: '',
            isEdit: false,//标识是否是修改
            form: {
                O_id: '',
                C_account_id: '',
                O_time: '',
                Ft_id_id: '',
                O_cost: '',
                M_id: '',
                M_name: '',
                M_num: '',
            },
            rules: {
            },
            total: 0,//数据总行数
            currentpage: 1,//当前页码
            pagesize: 8,//每页行数
            pagetable: [],//分页后当前页的数据
            tableData: [],//订单表格数据
            dishData: [],//所点菜品数据
            inputstr: '',//接收查询条件
            radio: '',
        };
    },
    methods: {
        //获取订单信息
        getOrderData: function () {
            //使用Ajax请求---post
            let that = this
            getOrder('已支付').then(function (res) {
                //请求成功
                if (res.data.code === 1) {
                    that.tableData = res.data.data
                    //获取当前返回记录的总行数
                    that.total = res.data.data.length
                    //获取当前页的数据
                    that.getPageData()
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
        //显示订单详情
        open_detail(row) {
            this.dialogTableVisible = true
            //使用Ajax请求---post
            let that = this
            getOrderDetail(row.O_id).then(function (res) {
                //请求成功
                if (res.data.code === 1) {
                    that.dishData = res.data.data
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
        //实现"全部"按钮功能
        getALLOrderData() {
            //清空查询条件
            this.inputstr = ''
            //获取全部数据
            this.getOrderData()
        },
        //查询员工信息
        queryOrderData() {
            if (this.inputstr === '') {
                this.$message({
                    message: '查询条件不能为空！',
                    type: 'warning'
                });
                return
            }
            //使用Ajax请求---post---传递inputstr
            let that = this
            queryOrder(that.inputstr, '已支付').then(function (res) {
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
        //删除订单信息
        deleteOrderData(row) {
            this.$confirm('是否确认删除该订单【订单号: ' + row.O_id + '\t账户: ' + row.C_account_id + '】的信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                //确认删除
                let that = this
                deleteOrder(row.O_id).then(res => {
                    //执行成功
                    if (res.data.code === 1) {
                        //获取所有订单信息
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
    },
    mounted() {
        this.getOrderData();
    },
    computed: {
        //控制按钮是否禁用
        isButtonDisabled() {
            this.radio = Cookie.get('radio')
            return this.radio === '0' ? false : true;
        },
    }
}
</script>