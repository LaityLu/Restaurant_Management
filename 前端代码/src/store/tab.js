import Cookie from "js-cookie"

export default{
    state:{
        isCollapse: false, // 控制菜单的展开还是收起
        tabsList: [
            //tabsList中存在某个item，面包屑就显示其标签，默认显示首页。
        ],//面包屑数据
        currentMenu:[],
        menuData:[]//左侧菜单数据
    },
    mutations: {
        // 修改菜单展开收起的方法
        collapseMenu(state) {
            state.isCollapse = !state.isCollapse
        },
        // 更新面包屑数据
        selectMenu(state, val) {
            // 判断添加的数据是否为首页，首页默认存在，若添加别的页面则触发
            if (val.label !== '首页') {
                state.currentMenu.splice(1, 1)
                state.currentMenu.push(val)
                //将添加的页面name与tabsList里面的页面name比较，若不存在，index=-1
                const index = state.tabsList.findIndex(item => item.name === val.name)
                // 如果不存在，将该页面item添加进tabsList中，更新面包屑
                if (index === -1) {
                    state.tabsList.push(val)
                }
            }
        },
        //设置默认的tag数据
        defaultTag(state,radio){
            state.tabsList = [];
            state.currentMenu = [];
            //默认显示首页。
            if(radio==='2'){
                var val ={
                    path: "/custhome",
                    name: "custhome",
                    label: "首页",
                    icon: "s-home",
                    url: "CustHome.vue",
                }
                state.tabsList.push(val)
                state.currentMenu.push(val)
            }else{
                var val ={
                    path: "/",
                    name: "home",
                    label: "首页",
                    icon: "s-home",
                    url: "Home.vue",
                }
                state.tabsList.push(val)
                state.currentMenu.push(val)
            }
        },
        // 删除指定的tag数据
        closeTag(state, item){
            if(item.label!=='首页'){
                  //找到指定的tag在tabsList中对应的索引
            const index = state.tabsList.findIndex(val => val.name === item.name)
            //从tabsList中删除
            state.tabsList.splice(index, 1)
            }
        },
        // 设置左侧菜单的数据
        setMenu(state, val) {
            state.menuData = val
            //将menuData经过JSON序列化后存入Cookie
            Cookie.set('menuData', JSON.stringify(val))
        },
        // 动态注册路由
        addMenu(state, router) {
            // 判断缓存中是否有数据, 即判断目前是否登录
            if (!Cookie.get('menuData')) return
            const menu = JSON.parse(Cookie.get('menuData'))
            state.menuData = menu
            // 组装动态路由的数据
            const menuArray = []
            menu.forEach(item => {
                if (item.children) {
                    item.children = item.children.map(item => {

                        item.component = () => import(`../views/${item.url}`)
                        return item
                    })
                    menuArray.push(...item.children)
                } else {

                    item.component = () => import(`../views/${item.url}`)
                    menuArray.push(item)
                }
            })
            // console.log('menuArray',menuArray)
            // 路由的动态添加
            menuArray.forEach(item => {
                router.addRoute('Main', item)
            })
        }
    }
}