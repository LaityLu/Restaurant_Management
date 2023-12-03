<template>
    <div style="padding-left:60px">
        <el-table :data="pagetable" :border="true" stripe style="width: 80%">
            <el-table-column prop="account" label="账号" width="180">
            </el-table-column>
            <el-table-column prop="Authority" label="身份权限" width="180">
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button type="success" size="mini" icon="el-icon-edit" @click="updateUserData(scope.row)">
                    </el-button>
                    <el-button type="danger" size="mini" icon="el-icon-delete" @click="deleteUserData(scope.row)">
                    </el-button>
                </template>
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
import { getUserData } from '@/api';
import { updateUser } from '@/api';
import { deleteUser } from '@/api';
export default {
    data() {
        return {
            total: 0,//数据总行数
            currentpage: 1,//当前页码
            pagesize: 8,//每页行数
            pagetable: [],//分页后当前页的数据
            tableData: [],//全部用户信息
        };
    },
    methods: {
        //获取顾客信息
        getUser: function () {
            let that = this//axios执行异步请求后,会让 this指向undefine
            getUserData().then(function (res) {
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
        //实现修改功能
        updateUserData(row) {
            let that = this
            let authority = ''
            if (row.authority === '0')
                authority = '1'
            else
                authority = '0'
            updateUser(row.account, authority).then(res => {
                //执行成功
                if (res.data.code === 1) {
                    //获取所有用户信息
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
        deleteUserData(row) {
            this.$confirm('是否确认删除该用户【账号: ' + row.account + '\t身份: ' + row.Authority + '】的信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                //确认删除
                let that = this
                deleteUser(row.account).then(res => {
                    //执行成功
                    if (res.data.code === 1) {
                        //获取所有用户信息
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
        this.getUser();
    },
};
</script>