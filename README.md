# 功能说明

------------

## 项目：电商平台([Eshop](https://github.com/Aoki-kelley/djangotest/tree/eshop))

*utf-8,python 3.9.7*

*基于django 3.2.8*

- 用户(买家) [^buyer]

​		1.包括字段：用户名，密码(未加密)，邮箱，头像，余额，

​			状态码[^on / off]，邮箱注册状态[^on / off]，角色[^seller / buyer]

​		2.可查看，收藏，下单，评论商品，回复商品的评论和回复

​		3.可取消卖家未处理的订单[^order.status=b_cancel]，或结束卖家结束的订单

- 用户(卖家)[^seller]

​		1.包括字段：用户名，密码(未加密)，邮箱，头像，交易额，

​			状态码[^on / off]，邮箱注册状态[^on / off]，角色[^seller / buyer]

​		2.可创建，上架，下架商品，回复评论和回复，不同卖家只能查看其他卖家的商品

​		3.可接受和拒绝[^order.status=s_cancel]用户的订单

- 商品[^goods]

​		1.包含字段：图像，商品名，商品描述(富文本)，标签，

​			创建时间，单价，库存，卖家id，状态码[^on / off]

​		2.库存未0时自动下架且不可被上架和下单

- 管理员[^admin]

​		1.可批量冻结用户[^status = off]，可解除冻结状态[^status = on]

​		2.可批量上架或下架商品

​		3.可按用户名检索用户

​		4.可按标签检索商品
