import Mock from 'mockjs'

export default{
    getDishList: () => {
        let tableData = []
        const count = 8
        for (let i = 0; i < count; i++) {
            tableData.push(
              Mock.mock({
                M_id: Mock.Random.increment(),
                M_name: '好滋好味鸡蛋仔',
                M_class: Mock.Random.integer(0, 3),
                'M_price|30-100': 30,
                })
            )
        }
        return {
            code:1000,
            data:{
                tableData,
            }
        }
    }   
}