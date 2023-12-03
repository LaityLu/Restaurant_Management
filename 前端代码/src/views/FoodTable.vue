<template>
    <div style="padding-left:60px">
        <!-- 提示窗 -->
        <el-dialog :title="dialogTitle" :before-close="handleClose" :visible.sync="dialogVisible" width="30%"
            :close-on-click-modal="false">
            <!-- 员工表单信息 -->
            <el-form ref="form" :rules="rules" :model="form" label-width="80px" label-position="right" style="width: 80%">
                <el-form-item label="餐桌号" prop="Ft_id">
                    <el-input placeholder="请输入餐桌号" :disabled="isEdit" v-model="form.Ft_id"
                        suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="座位数" prop="Ft_number">
                    <el-input placeholder="请输入座位数" v-model="form.Ft_number" suffix-icon="el-icon-edit"></el-input>
                </el-form-item>
                <el-form-item label="状态" prop="Ft_state">
                    <el-select placeholder="请选择状态" v-model="form.Ft_state" :disabled="!isEdit" style="width: 100%">
                        <el-option label="空闲" value="空闲"></el-option>
                        <el-option label="使用中" value="使用中"></el-option>
                        <el-option label="待清洁" value="待清洁"></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="submit">确 定</el-button>
                <el-button type="info" @click="cancel">取 消</el-button>
            </span>
        </el-dialog>
        <div>
            <el-button @click="addform()" type="primary" icon="el-icon-circle-plus-outline" style="margin-bottom: 20px"
                plain size="medium">新增
            </el-button>
            <el-table :data="pagetable" :border="true" :row-class-name="tableRowClassName" style="width: 60%"
                :default-sort="{ prop: 'Ft_state', order: 'descending' }">
                <el-table-column prop="Ft_id" label="餐桌号" width="180">
                </el-table-column>
                <el-table-column prop="Ft_number" label="座位数" width="180">
                </el-table-column>
                <el-table-column prop="Ft_state" label="状态" width="180">
                    <template slot-scope="scope">
                        <span>{{ scope.row.Ft_state }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button type="success" size="mini" icon="el-icon-edit" @click="updateform(scope.row)">
                        </el-button>
                        <el-button type="danger" size="mini" icon="el-icon-delete" @click="deleteFoodTableData(scope.row)">
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

<style  lang="less" scoped>
/deep/.el-table .warning-row {
    background: rgba(255, 220, 220, 0.7);
}

/deep/.el-table .success-row {
    background: rgba(211, 244, 194, 0.5);
}

/deep/.el-table .info-row {
    background: rgba(192, 196, 204, 0.5);
}
</style>


<script>
import { getFoodTable } from '@/api';
import { checkFtid } from '@/api'
import { addFoodTable } from '@/api'
import { updateFoodTable } from '@/api'
import { deleteFoodTable } from '@/api'
export default {
    data() {
        //校验餐桌号是否存在
        const rulesFt_id = (rules, value, callback) => {
            if (this.isEdit) {
                callback()
            }
            //使用Axios进行校验
            checkFtid(value).then(res => {
                //请求成功
                if (res.data.code === 1) {
                    if (res.data.exist) {
                        callback(new Error("餐桌号已存在！"))
                    } else {
                        callback()
                    }
                } else {
                    //请求失败
                    callback("后端校验编号出现异常！")
                }
            }).catch((err) => {
                console.log(err)
            })
        }
        return {
            dialogTitle: '',
            dialogVisible: false,
            isEdit: false,//标识是否是修改
            form: {
                Ft_id: '',
                Ft_number: '',
                Ft_state: '',
            },
            total: 0,//数据总行数
            currentpage: 1,//当前页码
            pagesize: 8,//每页行数
            pagetable: [],//分页后当前页的数据
            tableData: [],
            rules: {
                Ft_id: [
                    { required: true, message: "请输入餐桌号", trigger: 'blur', },
                    { pattern: /^\d+$/, message: "必须是数字", trigger: 'blur' },
                    { validator: rulesFt_id, trigger: 'blur' },
                ],
                Ft_number: [
                    { required: true, message: "请输入座位数", trigger: 'blur', },
                    { pattern: /^\d+$/, message: "必须是数字", trigger: 'blur' },
                ],
                Ft_state: [
                    { required: true, message: "请选择状态", trigger: 'change', },
                ],
            }
        };
    },
    methods: {
        //区分餐桌空闲、繁忙的状态，单独为某行设置属性
        tableRowClassName({ row, rowIndex }) {
            if (row.Ft_state === '使用中') {
                //使用中
                return 'warning-row';
            } else if (row.Ft_state === '空闲') {
                //空闲
                return 'success-row';
            } else if (row.Ft_state === '待清洁') {
                //待清洁
                return 'info-row';
            }
            return '';
        },
        //获取餐桌信息
        getFoodTableData: function () {
            let that = this//axios执行异步请求后,会让 this指向undefine
            getFoodTable().then(function (res) {
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
        //"添加餐桌"表单
        addform() {
            //修改标题
            this.dialogTitle = "添加新餐桌"
            //弹出表单
            this.dialogVisible = true
            this.form.Ft_state = '空闲'
        },
        //"修改餐桌"表单
        updateform(row) {
            //修改标题
            this.dialogTitle = "修改餐桌信息"
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
                        this.updateFoodTableData()
                    }
                    else {
                        //添加
                        this.addFoodTableData(formData)
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
        //添加新餐桌
        addFoodTableData(formData) {
            let that = this
            addFoodTable(formData).then(res => {
                //执行成功
                if (res.data.code === 1) {
                    //获取所有餐桌信息
                    that.tableData = res.data.data
                    //获取当前返回记录的总行数
                    that.total = res.data.data.length
                    //获取当前页的数据
                    that.getPageData()
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
        updateFoodTableData() {
            let that = this
            console.log(that.form.Ft_state)
            updateFoodTable(that.form).then(res => {
                //执行成功
                if (res.data.code === 1) {
                    //获取所有餐桌信息
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
        deleteFoodTableData(row) {
            this.$confirm('是否确认删除该餐桌号【餐桌号: ' + row.Ft_id + '\t座位数: ' + row.Ft_number + '】的信息？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                //确认删除
                let that = this
                deleteFoodTable(row.Ft_id).then(res => {
                    //执行成功
                    if (res.data.code === 1) {
                        //获取所有餐桌信息
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
        this.getFoodTableData();
    }
};
</script>