<!--导航菜单组件-->
<template>
    <el-menu default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
        :collapse="isCollapse" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
        <h3>{{ isCollapse ? aName[1] : aName[0] }}</h3>
        <!-- 一级菜单 -->
        <el-menu-item @click="clickMenu(item)" v-for="item in noChildren" :key="item.name" :index="item.name">
            <i :class="`el-icon-${item.icon}`"></i>
            <span slot="title">{{ item.label }}</span>
        </el-menu-item>
        <!-- 二级菜单 -->
        <el-submenu v-for="item in hasChildren" :key="item.label" :index="item.label">
            <template slot="title">
                <i :class="`el-icon-${item.icon}`"></i>
                <span slot="title">{{ item.label }}</span>
            </template>
            <!-- 子菜单 -->
            <el-menu-item-group v-for="subItem in item.children" :key="subItem.path">
                <el-menu-item @click="clickMenu(subItem)" :index="subItem.path">
                    <i :class="`el-icon-${subItem.icon}`"></i>
                    <span slot="title">{{ subItem.label }}</span>
                </el-menu-item>
            </el-menu-item-group>
        </el-submenu>
    </el-menu>
</template>


<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu {
    height: 100vh;

    h3 {
        color: #fff;
        text-align: center;
        line-height: 48px;
        font-size: 16px;
        font-weight: 400;
    }
}
</style>
    
<script>
import Cookie from 'js-cookie';

export default {
    data() {
        return {
        };
    },
    methods: {
        //控制左侧父导航栏展开子导航栏
        handleOpen(key, keyPath) {
            // console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            // console.log(key, keyPath);
        },
        //点击导航菜单
        clickMenu(item) {
            // console.log(item, 'Aside');
            //1、只有当前页面的路由与要跳转的路由不一致时才跳转
            //2、由于有重定向，将'/'重定向为'/home'，所以如果从'/home'跳转到'/'会报错，要加条件
            if (this.$route.path !== item.path && !(this.$route.path === '/home' && (item.path === '/'))) {
                this.$router.push(item.path);//跳转
            }
            //调用"store/tab/mutations:selectMenu"，实现面包屑功能
            this.$store.commit('selectMenu', item)
        }
    },
    computed: {
        //没有子菜单
        noChildren() {
            return this.menuData.filter(item => !item.children)
        },
        //有子菜单
        hasChildren() {
            return this.menuData.filter(item => item.children)
        },
        //定义左侧导航栏展开或者关闭的属性
        isCollapse() {
            return this.$store.state.tab.isCollapse
        },
        //设置左侧菜单数据
        menuData() {
            //如果Cookie中存在menData则从Cookie中获取，否则从store中获取
            return JSON.parse(Cookie.get('menuData')) || this.$store.state.tab.menuData
        },
        //设置名称
        aName() {
            const radio = Cookie.get("radio")
            if (radio === '2') {
                return ["餐厅用户系统", "用户"]
            } else {
                return ["餐厅管理系统", "管理"]
            }
        }
    }
}
</script>

<style lang="less" scoped>
.el-menu {
    border-right: none;
}
</style>