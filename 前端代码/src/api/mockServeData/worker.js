import Mock from 'mockjs'

export default{
    getWorkerList: () => {
        let tableData = []
        const count = 8
        for (let i = 0; i < count; i++) {
            tableData.push(
                Mock.mock({
                W_id: Mock.Random.id(),
                W_name: Mock.Random.cname(),
                W_sex: Mock.Random.integer(0, 1),
                'W_age|18-60': 18,
                W_birth: "@date('yyyy-MM-dd')",
                W_addr: "@county(true)",
                W_phone: /^1(5|3|7|8)[0-9]{9}$/,
                W_job: Mock.Random.integer(0, 1),
                W_salary: Mock.Random.increment(1000),
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