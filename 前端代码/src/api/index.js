import http from '../utils/request.js'

// 请求首页数据
export const getData = () => {
    // 返回一个promise对象
    return http.get('/home/getData')
}

//请求餐桌数据
export const getFoodTable = () => {
    // 返回一个promise对象
    return http.get('foodTable/')
}

//校验餐桌号
export const checkFtid = (value) => {
    // 返回一个promise对象
    return http.post('foodTable/check/',{
        Ft_id: value,
    })
}

//添加餐桌信息
export const addFoodTable = (value) => {
    // 返回一个promise对象
    return http.post('foodTable/add/',{
        Ft_id: value.Ft_id,
        Ft_number: value.Ft_number,
    })
}

//修改餐桌信息
export const updateFoodTable = (value) => {
    // 返回一个promise对象
    return http.post('foodTable/update/',{
        Ft_id: value.Ft_id,
        Ft_number: value.Ft_number,
        Ft_state: value.Ft_state,
    })
}

//删除餐桌信息
export const deleteFoodTable = (value) => {
    // 返回一个promise对象
    return http.post('foodTable/delete/',{
        Ft_id: value,
    })
}

//请求菜品数据
export const getDish = () => {
    // 返回一个promise对象
    return http.get('dish/')
}

//查询菜品数据
export const queryDish = (inputstr) => {
    // 返回一个promise对象
    return http.post('dish/query/',{
        inputstr:inputstr
    })
}

//校验菜品编号
export const checkDid = (value) => {
    // 返回一个promise对象
    return http.post('dish/check/',{
        M_id: value,
    })
}

//添加菜品信息
export const addDish = (value) => {
    // 返回一个promise对象
    return http.post('dish/add/',{
        M_id: value.M_id,
        M_name: value.M_name,
        M_class: value.M_class,
        M_price: value.M_price,
    })
}

//修改菜品信息
export const updateDish = (value) => {
    // 返回一个promise对象
    return http.post('dish/update/',{
        M_id: value.M_id,
        M_name: value.M_name,
        M_class: value.M_class,
        M_price: value.M_price,
    })
}

//删除菜品信息
export const deleteDish = (value) => {
    // 返回一个promise对象
    return http.post('dish/delete/',{
        M_id: value,
    })
}

//将信息导入Excel
export const exportToExcel = (value) => {
    // 返回一个promise对象
    return http.post('excel/export/',{
        name: value,
    })
}

//请求顾客数据
export const getCustomer = () => {
    // 返回一个promise对象
    return http.get('customer/')
}

//查询顾客数据
export const queryCustomer = (inputstr) => {
    // 返回一个promise对象
    return http.post('customer/query/',{
        inputstr:inputstr
    })
}

//请求员工数据
export const getWorker = () => {
    // 返回一个promise对象
    return http.get('worker/')
}

//查询员工数据
export const queryWorker = (inputstr) => {
    // 返回一个promise对象
    return http.post('worker/query/',{
        inputstr:inputstr
    })
}

//校验员工工号
export const checkWid = (value) => {
    // 返回一个promise对象
    return http.post('worker/check/',{
        W_id: value,
    })
}

//添加员工信息
export const addWorker = (value) => {
    // 返回一个promise对象
    return http.post('worker/add/',{
        W_id: value.W_id,
        W_name: value.W_name,
        W_sex: value.W_sex,
        W_birth: value.W_birth,
        W_addr: value.W_addr,
        W_phone: value.W_phone,
        W_job: value.W_job,
        W_salary: value.W_salary,
    })
}

//修改员工信息
export const updateWorker = (value) => {
    // 返回一个promise对象
    return http.post('worker/update/',{
        W_id: value.W_id,
        W_name: value.W_name,
        W_sex: value.W_sex,
        W_birth: value.W_birth,
        W_addr: value.W_addr,
        W_phone: value.W_phone,
        W_job: value.W_job,
        W_salary: value.W_salary,
    })
}

//删除员工信息
export const deleteWorker = (value) => {
    // 返回一个promise对象
    return http.post('worker/delete/',{
        W_id: value,
    })
}

//请求订单数据
export const getOrder = (str) => {
    // 返回一个promise对象
    return http.post('order/', {O_state:str})
}

//请求订单详细数据
export const getOrderDetail = (value) => {
    // 返回一个promise对象
    return http.post('order/detail/', {O_id:value})
}

//查询订单信息
export const queryOrder = (inputstr,state) => {
    // 返回一个promise对象
    return http.post('order/query/',{
        inputstr:inputstr,
        state:state,
    })
}

//删除订单详细数据
export const deleteOrder = (value) => {
    // 返回一个promise对象
    return http.post('order/delete/', {O_id:value})
}

//完成订单
export const finishOrder = (value) => {
    // 返回一个promise对象
    return http.post('order/finish/', {O_id:value})
}

//校验用户名
export const checkUsername = (value) => {
    // 返回一个promise对象
    return http.post('register/check/',{
        username:value,
    })
}

//用户注册
export const register = (username,password) => {
    // 返回一个promise对象
    return http.post('/register/', {
        username:username,
        password:password,
    })
}

//用户登录
export const login = (username,password,radio) => {
    return http.post('/login/', {
        username:username,
        password:password,
        radio:radio
    })
}

//用户修改密码
export const modifyPassword = (username,password) => {
    return http.post('/home/modifypassword/', {
        username:username,
        password:password,
    })
}

//获取首页数据
export const getHomeData = () => {
    return http.get('home/')
}

//获取首页数据
export const getUserData = () => {
    return http.get('manage/')
}

//更新用户数据
export const updateUser = (account,authority) => {
    return http.post('manage/update/', {
        account:account,
        authority:authority,
    })
}

//删除用户数据
export const deleteUser = (account) => {
    return http.post('manage/delete/', {
        account:account,
    })
}