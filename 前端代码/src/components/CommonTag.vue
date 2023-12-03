<template>
    <div class="tags">
        <el-tag v-for="(item, index) in tags" :key="item.path" :closable="item.label !== '首页'" :type="item.type"
            :effect="$route.name === item.name ? 'dark' : 'plain'" @click="changeMenu(item)"
            @close="handleClose(item, index)" size="small">
            {{ item.label }}
        </el-tag>
    </div>
</template>

<script>
import router from '@/router';
import Cookie from 'js-cookie';
import { mapState } from 'vuex';

export default {
    created() {
        this.$store.commit('defaultTag', Cookie.get('radio'));
    },
    name: 'CommomTag',
    data() {
        return {}
    },
    computed: {
        //利用辅助函数获取state中的tabsList
        ...mapState({
            tags: (state) => state.tab.tabsList
        })
    },
    methods: {
        //通过点击tag标签来跳转页面
        changeMenu(item) {
            //1、只有当前页面的路由与要跳转的路由不一致时才跳转
            //2、由于有重定向，将'/'重定向为'/home'，所以如果从'/home'跳转到'/'会报错，要加条件
            if (this.$route.path !== item.path && !(this.$route.path === '/home' && (item.path === '/'))
            ) {
                this.$router.push(item.path);//跳转
            }
        },
        //实现删除tag标签并跳转、高亮显示当前页面对应标签
        handleClose(item, index) {
            this.$store.commit('closeTag', item)
            //length为删除指定标签后所剩标签个数
            const length = this.tags.length
            // console.log(length)
            // 删除的标签与当前显示的页面不对应，不用跳转，也不用处理
            if (item.name !== this.$route.name) {
                // console.log(1)
                return
            }
            // 表示删除的对应当前显示页面并且是最后一项标签，需要跳转到相邻的上一个标签对应页面
            if (index === length) {
                // console.log(2)
                this.$router.push({
                    name: this.tags[index - 1].name
                })
            } else {
                // 表示删除的对应当前显示页面但不是最后一项标签，需要跳转到相邻的下一个标签对应页面
                // console.log(3)
                this.$router.push({
                    name: this.tags[index].name
                })
            }
        }
    }
}
</script>

<style lang="less" scoped>
.tags {
    padding-top: 20px;
    padding-inline: 20px;
    margin-bottom: 1px;

    .el-tag {
        margin-right: 15px;
        cursor: pointer;
    }
}
</style>