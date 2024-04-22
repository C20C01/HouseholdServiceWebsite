# 家政服务网站

一个使用**Django**框架开发的家政服务网站，实现了下单、接单、评价等功能。

*⚠ 仅作为 ~~作业~~ 练习项目，不具备实际使用价值。*

## 结构

类似于外卖、网约车等服务的模式；用户发布需求，家政员接单。

* 客户
    * 新建订单
    * 查看当前订单
    * 查看历史订单
    * 评价服务
* 家政员
    * 接受订单
* 管理员
    * 查看客户、家政员、订单信息

## 入口

* 客户：`/customer/`（用户名：111，密码：111）
* 家政员：`/worker/`（用户名：222，密码：222）
* 后台：`/backend/`（用户名：cc，密码：cc）

要同时登录多个账号，可以使用不同的浏览器或隐身模式。

## 截图

<details>
<summary>首页</summary>

![home.png](img/home.png)
</details>

<details>
<summary>新建订单</summary>

![new_order.png](img/new_order.png)
</details>

<details>
<summary>当前订单——客户端（等待接单）</summary>

![current_order_1.png](img/current_order_1.png)
</details>

<details>
<summary>挑选订单</summary>

![accept_order.png](img/accept_order.png)
</details>

<details>
<summary>当前订单——员工端</summary>

![accepted_order.png](img/accepted_order.png)
</details>

<details>
<summary>当前订单——客户端（服务中）</summary>

![current_order_2.png](img/current_order_2.png)
</details>

<details>
<summary>评价订单</summary>

![review.png](img/review.png)
</details>

<details>
<summary>历史订单</summary>

![history_order.png](img/history_order.png)
</details>

<details>
<summary>订单信息——后台</summary>

![backend_order.png](img/backend_order.png)
</details>

<details>
<summary>员工信息——后台</summary>

![backend_worker.png](img/backend_worker.png)
</details>
