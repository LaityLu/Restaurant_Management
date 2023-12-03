import Mock from 'mockjs'

// get请求从config.url获取参数，post从config.body中获取参数
// function param2Obj(url) {
//   const search = url.split('?')[1]
//   if (!search) {
//     return {}
//   }
//   return JSON.parse(
//     '{"' +
//     decodeURIComponent(search)
//       .replace(/"/g, '\\"')
//       .replace(/&/g, '","')
//       .replace(/=/g, '":"') +
//     '"}'
//   )
// }

// let tableData = []
// const count = 8
export default{
    getCustomerList: () => {
        let tableData = []
        const count = 8
        for (let i = 0; i < count; i++) {
            tableData.push(
                Mock.mock({
                C_id: Mock.Random.id(),
                C_name: Mock.Random.cname(),
                C_sex: Mock.Random.integer(0, 1),
                C_phone: /^1(5|3|7|8)[0-9]{9}$/,
                'C_ordernum|10-60': 1,
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