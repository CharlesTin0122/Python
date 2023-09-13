# 零基础理解四元数，每个游戏入门开发必备知识

谢鱼 于 2021-10-27 22:38:20 发布
[csdn原地址](https://blog.csdn.net/weixin_40137140/article/details/120888190?spm=1001.2014.3001.5502)
原贴的数学公式没有使用LaTex数学公式，顾数学公式部分看上去有些混乱。这里用LaTex重新编写了数学公式，修复了一些错误。
---
## 复数

在我们能够完全理解四元数之前，我们必须先知道四元数是怎么来的。四元数的根源其实是复数。

除了知名的数集（自然数、整数、实数、分数）之外，复数系统引入了一个新的数集——虚数。虚数的发明是为了解决一些特定的无解的方程，例如：

$$x^2+1=0$$

要解决这个等式，必须让 $x^2=−1$ ，这当然是不行的，因为任意实数的平方都是非负数。

一般而言，数学家是不能忍受一个等式是无解的。于是，一个新的术语被发明了，它就是虚数，一个可以解决上面这个等式的数。

虚数有这样的形式：

$$i^2=−1$$

不要为这个术语较真，因为逻辑上这个数是不存在的。只要知道i是一个平方等于-1的东西即可。

虚数的集合可以用 𝕀 来表示。复数的集合ℂ 是一个实数和一个虚数的和，形式如下：

$$
z=a+bi\\
a,b∈\mathbb{R},  i^2=−1
$$

可以认为所有实数都是 $b=0$ 的复数、所有虚数都是$a=0$的复数。

### 复数的加法：
$$
(a_1+b_1i)+(a_2+b_2i)=(a_1+a_2)+(b_1+b_2)i
$$
### 复数的减法：
$$
(a_1+b_1i)−(a_2+b_2i)=(a_1−a_2)+(b_1−b_2)i
$$
### 复数的系数缩放
$$
\lambda(a_1+b_1i)=\lambda a_1+\lambda b_1i
$$
### 复数的积
$$
\begin{aligned}
z_1&=(a_1+b_1i)\\
z_2&=(a_2+b_2i)\\
z_1z_2&=(a_1+b_1i)(a_2+b_2i)=a_1a_2+a_1b_2i+b_1a_2i+b_1b_2i^2\\
z_1z_2&=(a_1a_2−b_1b_2)+(a_1b_2+b_1a_2)i
\end{aligned}
$$
### 复数的平方
$$
\begin{aligned}
z&=(a+bi)\\
z^2&=(a+bi)(a+bi)\\
z^2&=(a^2−b^2)+2abi
\end{aligned}
$$
### 共轭复数

复数的共轭就是指把复数的虚数部分变成负的。共轭复数的符号是z¯ 或 z∗
$$
z=(a+bi)\\
z^∗=(a−bi)
$$
### 复数和它的共轭复数的乘积：
$$
zz^∗=(a+bi)(a−bi)=a^2−abi+abi+b^2=a^2+b^2
$$
### 复数的绝对值

我们使用共轭复数来计算复数的绝对值：
$$
\begin{aligned}
z=&(a+bi)\\
|z|=&\sqrt{zz^∗}=\sqrt{(a+bi)(a−bi)}=\sqrt{a^2+b^2}
\end{aligned}
$$
### 两复数的商
运算方法：可以把除法换算成乘法做，在分子分母同时乘上分母的共轭。所谓共轭你可以理解为加减号的变换，互为共轭的两个复数相乘是个实常数。
$$
\begin{aligned}
\frac{a+bi}{c+di}=&\frac{(a+bi)(c−di)}{(c+di)(c−di)}\\
=&\frac{(ac+bd)+(bc-ad)i}{c^2+d^2}\\
=&\frac{ac+bd}{c^2+d^2}+\frac{bc-ad}{c^2+d^2}*i\\
\end{aligned}
$$
### i的幂

如果i的平方等于-1，那么i的n次幂也应该存在：
$$
\begin{aligned}
i^0&=1\\
i^1&=i\\
i^2&=−1\\
i^3&=ii^2=−i\\
i^4&=i^2i^2=1\\
i^5&=ii^4=i\\
i^6&=ii^5=i^2=−1
\end{aligned}
$$
如果按照这个顺序写下去，会出现这样一个模式：
$$(1,i,-1,-i,1,…)$$

一个类似的模式也出现在递增的负数幂：
$$
\begin{aligned}
i^0&=1\\
i^−1&=−i\\
i^−2&=−1\\
i^−3&=i\\
i^−4&=1\\
i^−5&=−i\\
i^−6&=−1\\
\end{aligned}
$$
你可能已经在数学里头见过类似的模式，但是是以$（x,y,-x,-y,x,…)$的形式，这是在2D笛卡尔平面对一个点逆时针旋转90度时生成的；$（x,-y,-x,y,x,…)$则是在2D笛卡尔平面对一个点顺时针旋转90度时生成的。

![在这里插入图片描述](https://img-blog.csdnimg.cn/40010053554f4d87bd03e681a412206e.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6LCi6bG8,size_20,color_FFFFFF,t_70,g_se,x_16)

### 复数平面
我们也能够把复数映射到一个2D网格平面——复数平面，只需要把实数映射到横轴、虚数映射到纵轴。

![](https://img-blog.csdnimg.cn/15424816b1a243feb7af0c695fe9bf52.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6LCi6bG8,size_20,color_FFFFFF,t_70,g_se,x_16)

如前面的序列所示，我们可以认为，对一个复数乘以i，这个复数就在复数平面上旋转了90度。

让我们看看这是不是真的。我们随机地在复数平面上取一个点：
$$
p=2+i
$$
p乘以i后得到q：
$$
q=p*i=(2+i)*i=2i+i^2=−1+2i
$$
q乘以i后得到r：
$$
r=q*i=(−1+2i)*i=−i+2i^2=−2−i
$$
r乘以i后得到s：
$$
s=r*i=(−2−i)*i=−2i−i^2=1−2i
$$
s乘以i后得到t：
$$
t=s*i=(1−2i)*i=i−2i^2=2+i
$$
t刚好是开始的p。如果我们把这些复数放到复数平面上，就得到下面的图：

![旋转过程结果](https://img-blog.csdnimg.cn/7abb378054f1474bb0363467e279fa73.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6LCi6bG8,size_20,color_FFFFFF,t_70,g_se,x_16)

我们也可以按顺时针方向旋转，只需要把上面的乘数i改成-i。

### 旋转数（Rotators)
我们也可以在复数平面上进行任意角度的旋转，只需要定义下面这个复数，改变θ角旋转任意度：

特殊的复数 旋转数公式: 
$$
q=cosθ+sinθ*i
$$
任意的复数乘以q：
$$
\begin{aligned}
p&=a+bi\\
q&=cosθ+sinθ*i\\
pq&=(a+bi)(cosθ+sinθi)\\
a^′+b^′i&=acosθ−bsinθ+(asinθ+bcosθ)i
\end{aligned}
$$
也可以写成矩阵的形式：
$$
[a′b′−b′a′]=[cosθsinθ−sinθcosθ][ab−ba] 
$$
这也是一个在复数平面绕原点逆时针旋转任意点的方法。（译注：这句话应该是在说旋转矩阵）

## 四元数
了解了复数系统和复数平面后，我们可以额外增加2个虚数到我们的复数系统，从而把这些概念拓展到3维空间。

四元数的一般形式：
$$
q=s+xi+yj+zk \\
s,x,y,z∈\mathbb{R}
$$
上面的公式是根据Hamilton的著名的表达式得到的：
$$
i^2=j^2=k^2=ijk=−1
$$
以及：
$$
\begin{aligned}
ij&=k\\
jk&=i\\
ki&=j\\
ji&=−k\\
kj&=−i\\
ik&=−j
\end{aligned}
$$
你可能已经注意到了，i、j、k之间的关系非常像笛卡尔坐标系下单位向量的叉积规则：
即两个单位向量的叉积等于垂直于这两个向量的单位向量。
$$
\begin{aligned}
x×y&=z\\
y×z&=x\\
z×x&=y\\
y×x&=−z\\
z×y&=−x\\
x×z&=−y\\
\end{aligned}
$$
Hamilton自己也发现i、j、k虚数可以被用来表达3个笛卡尔坐标系单位向量i、j、k，并且仍然保持有虚数的性质，也即$i^2=j^2=k^2=−1$。

（i x j, j x k,k x i ,这几个性质的可视化）(x代表叉乘)

![过程](https://img-blog.csdnimg.cn/2dc9ad70ebc24952afed2e4390a32c07.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6LCi6bG8,size_20,color_FFFFFF,t_70,g_se,x_16)

上图展示了如何用i、j、k作为笛卡尔坐标系的单位向量。

作为有序数的四元数

我们可以用有序对的形式，来表示四元数：
$$
[s,v],s \in \mathbb{R}, v \in \mathbb{R}^3
$$
其中的v，也可以用它各自独立的3个分量表示：
$$
q=[s,xi+yj+zk]\\
 s,x,y,z \in \mathbb{R}
$$
使用这种表示法，我们可以更容易地展示四元数和复数之间的相似性。

### 四元数的加减

和复数类似，四元数也可以被加减：
$$
\begin{aligned}
q_a&=[s_a,a]\\
q_b&=[s_b,b]\\
q_a+q_b&=[s_a+s_b,a+b]\\
q_a−q_b&=[s_a−s_b,a−b]\\
\end{aligned}
$$
### 四元数的积

我们也可以表示四元数的乘积：
$$
\begin{aligned}
q_aq_b&=[s_a,a][s_b,b]\\
&=(s_a+x_ai+y_aj+z_ak)(s_b+x_bi+y_bj+z_bk)\\
&=(s_as_b−x_ax_b−y_ay_b−z_az_b)\\
&+(s_ax_b+s_bx_a+y_az_b−y_bz_a)i\\
&+(s_ay_b+s_by_a+z_ax_b−z_bx_a)j\\
&+(s_az_b+s_bz_a+x_ay_b−x_by_a)k
\end{aligned}
$$
可以看到，四元数的乘积依然还是一个四元数。如果我们把虚数i、j、k

替换成有序对：
$$
i=[0,i]\\ j=[0,j]\\ k=[0,k]
$$
以及还有$[1,0] = 1$，将它们代入前面的表达式，就得到了：
$$
q_aq_b=(s_as_b−x_ax_b−y_ay_b−z_az_b)[1,0]\\
+(s_ax_b+s_bx_a+y_az_b−y_bz_a)[0,i]\\
+(s_ay_b+s_by_a+z_ax_b−z_bx_a)[0,j]\\
+(s_az_b+s_bz_a+x_ay_b−x_by_a)[0,k]
$$
再把这个表达式扩展成多个有序对的和：
$$
q_aq_b=[(s_as_b−x_ax_b−y_ay_b−z_az_b),0]\\
+[0,(s_ax_b+s_bx_a+y_az_b−y_bz_a)i]\\
+[0,(s_ay_b+s_by_a+z_ax_b−z_bx_a)j]\\
+[0,(s_az_b+s_bz_a+x_ay_b−x_by_a)k]
$$
如果把后3个四元数相加，并提取公共部分，就可以把等式改写成：
$$
\begin{aligned}
q_aq_b&=[(s_as_b−x_ax_b−y_ay_b−z_az_b),0]\\
&+[0,s_a(x_bi+y_bj+z_bk)+s_b(x_ai+y_aj+z_ak)\\
&+(y_az_b−y_bz_a)i+(z_ax_b−z_bx_a)j+(x_ay_b−x_by_a)k]
\end{aligned}
$$
这个等式是2个有序对的和。第1个有序对是一个实四元数，第2个是一个纯四元数。这两个四元数也可以合并成一个：
$$
\begin{aligned}
q_aq_b=&[(s_as_b−x_ax_b−y_ay_b−z_az_b),\\
&s_a(x_bi+y_bj+z_bk)+sb(x_ai+y_aj+z_ak)\\
&+(y_az_b−y_bz_a)i+(z_ax_b−z_bx_a)j+(x_ay_b−x_by_a)k]\\
\end{aligned}
$$
如果把下面的表达式代入上面的等式：
$$
\begin{aligned}
a&=x_ai+y_aj+z_ak\\
b&=x_bi+y_bj+z_bk\\
a⋅b&=x_ax_b+y_ay_b+z_az_b\\
a×b&=(y_az_b−y_bz_a)i+(z_ax_b−z_bx_a)j+(x_ay_b−x_by_a)k
\end{aligned}
$$
（译注：注意，第三条和第四条并不是四元数的点积和叉积，而是向量的点积和叉积）

我们就得到了：

**四元数的乘积一般式**： 
$$
q_aq_b=[s_as_b−a⋅b,s_ab+s_ba+a×b]
$$
这就是四元数乘积的一般式。

### 实四元数

一个实四元数是一个虚部向量为零向量的四元数：
$$
q=[s,0]
$$
两个实四元数的乘积是另一个实四元数：
$$
q_a=[s_a,0]\\
q_b=[s_b,0]\\
q_aq_b=[s_a,0][s_b,0]=[s_as_b,0]
$$
这和2个虚部为0的复数的乘积几乎一样：
$$
z_1=a_1+0i\\
z_2=a_2+0i\\
z_1z_2=(a_1+0i)(a_2+0i)=a_1a_2
$$
### 四元数的系数缩放

我们也可以用一个系数（实数）去乘四元数：
$$
q=[s,v]\\
λq=λ[s,v]=[λs,λv]
$$
我们可以用实四元数与普通四元数的乘积，来确认这个等式是否正确：
$$
q=[s,v]\\
λ=[λ,0]\\
λq=[λ,0][s,v]=[λs,λv]
$$
### 纯四元数

和实四元数相似，Hamilton也定义了纯四元数。纯四元数是s=0的四元数：
$$
q=[0,v]
$$
也可以写成下面的形式：
$$
q=xi+yk+zk
$$
然后是2个纯四元数的乘积：
$$
q_a=[0,a]\\
q_b=[0,b]\\
q_aq_b=[0,a][0,b]=[−a⋅b,a×b]
$$
### 四元数的加法形式

我们可以把四元数写成实四元数和纯四元数的和：
$$
q=[s,v]
=[s,0]+[0,v]
$$
### 单位四元数

给定任意的向量v，我们可以把这个向量写成一个系数和一个单位方向向量的乘积：
$$
V=u \hat{V}\\
v=|V|\\
|\hat{V}|=1
$$
将这个定义和纯四元数的定义结合，就得到了：
$$
q=[0,V]\\
=[0,v\hat{V}]\\
=v[0,\hat{V}]
$$
然后，我们可以定义单位四元数了，它是一个s=0、v

为单位向量的四元数：
$$
q̂=[0,\hat{V}]
$$
### 四元数的二元形式

我们现在可以把单位四元数的定义和四元数的加法形式结合到一起，就创造了一种新的四元数的表示法，这种表示法和复数的表示法形似：
$$
\begin{aligned}
q&=[s,v]\\
&=[s,0]+[0,v]\\
&=[s,0]+v[0,v̂]\\
&=s+vq̂
\end{aligned}
$$
这就给了我们一种和复数非常相似的四元数表示法：
```math
z=a+bi\\
q=s+vq̂
```
### 共轭四元数

共轭四元数的计算，就是将四元数的虚向量取反：
$$
q=[s,v]\\
q^∗=[s,−v]
$$
四元数和它的共轭四元数的乘积：
```math
\begin{aligned}
qq^∗&=[s,v][s,−v]\\
&=[s^2−v⋅(−v),−sv+sv+v×(−v)]\\
&=[s^2+v⋅v,0]\\
&=[s^2+v^2,0]
\end{aligned}
```
### 四元数范数（类似向量模长，但是定义不一样）

回忆下复数范数的定义：
$$
|z|=\sqrt{a2+b2}\\
zz^∗=|z|^2
$$
类似的，四元数的范数可以这样定义：
$$
q=[s,v]\\
|q|=\sqrt{s^2+v^2}
$$
这也让我们可以这样表达四元数范数：
$$
qq^∗=|q|^2
$$
### 四元数规范化（类似向量归一化）

利用四元数范数的定义，就可以对四元数进行归一化。要让一个四元数归一化，只需要让这个四元数去除以它的范数（模长）：
```math
q′=\frac{q}{\sqrt{s^2+v^2}}
```

举一个例子，让我们规范化下面这个四元数：

```math
q=[1,4i+4j−4k]
```

第一步，先计算q的范数：

```math
|q|=\sqrt{1^2+4^2+4^2+(−4)^2}=\sqrt{49}=7
```

然后，q除以|q|:
```math
\begin{aligned}
q′&=q / |q|\\
&=\frac{1+4i+4j−4k}{7}\\
&=1/7+(4/7)i+(4/7)j−(4/7)k
\end{aligned}
```
### 四元数的逆

四元数的逆用$q^−1$,因为电脑符号不方便，请仔细区分表示。
要计算四元数的逆，需要**用四元数的共轭四元数去除以四元数的范数的平方**：
```math
q^−1=\frac{q^*}{|q|^2}
```
为了证明这个式子，我们先根据逆的定义，有：
```math
qq^−1=[1,0]=1
```
两边都左乘共轭四元数q∗:
```math
q^∗qq^−1=q^∗
```
将上文中的$qq^∗=|q|^2$

代入这个式子，得到：
```math
|q|^2q^−1=q^∗\\
q^−1=\frac{q^∗}{|q|^2}
```
对于单位四元数，它的范数是1，所以可以写成：
```math
q^−1=q^∗
```
### 四元数的点积

和向量的点积相似，我们也可以计算2个四元数的点积，只需要将各个对应的系数相乘，然后相加:
```math
q_1=[s_1,x_1i+y_1j+z_1k]\\
q_2=[s_2,x_2i+y_2j+z_2k]
```
四元数的点积公式: 
```math
q_1⋅q_2=s_1s_2+x_1x_2+y_1y_2+z_1z_2
```
我们也可以利用四元数点积，来计算四元数之间的角度差(夹角)：
```math
cosθ=\frac{s_1s_2+x_1x_2+y_1y_2+z_1z_2}{|q_1||q_2|}
```
对于**单位四元数**，我们可以简化上面的等式：
```math
cosθ=s_1s_2+x_1x_2+y_1y_2+z_1z_2
```
### 四元数旋转

前面我们定义了一个特殊的复数：旋转数。它是用来旋转2D复数平面的点的：
```math
q=cosθ+sinθ*i
```
根据四元数和复数的相似性，应该有可能设计一个可以旋转3D空间的点的四元数：
```math
q=[cosθ,sinθ*V]
```
让我们测试一下这个理论是否可靠，方法就是计算四元数q和向量p的积。
第一步，我们把p写成纯四元数的形式：
```math
p=[0,p]
```
以及单位四元数q：
```math
q=[s,λv̂]
```
从而：
```math
p′ = qp = [s,λv̂][0,p]
```
代入四元数的乘积一般式： $q_aq_b=[s_as_b−a⋅b,s_ab+s_ba+a×b]$

得出：
```math
p′ = [−λv̂⋅p,sp+λv̂×p]
```
我们可以看到结果是一个同时有系数、有虚向量的四元数。

让我们先考虑特殊的情形：p与v̂正交(向量p垂直于单位向量v)。
这种情况下，点乘部分等于0：$−λv̂⋅p=0$

所以上面的四元数就变成了纯四元数：
```math
p′=[0,sp+λv̂×p]
```
这时候，要使p

绕v̂旋转，我们只需要代入$s=cosθ$和$λ=sinθ$：
```math
p′=[0,cosθp+sinθv̂×p]
```
现在，让我们找一个例子来测试上面的公式。譬如绕z轴(就是k轴)旋转向量 p 到45°，那么我们的四元数q就变为:
```math
\begin{aligned}
q&=[cosθ,sinθk]\\
&=[\frac{\sqrt{2}}{2},\frac{\sqrt{2}}{2}k]
\end{aligned}
```
然后，选一个特殊的p，并且p要和k轴正交(p垂直于向量k,四元数空间中的k轴),譬如把p放到i轴上，也就是：
```math
p=[0,2i]
```
现在我们可以求取q与p的乘积:
```math
p′=qp
```
此处代入四元数的乘积一般式
```math
\begin{aligned}
p′&=qp\\
&=[\frac{\sqrt{2}}{2},\frac{\sqrt{2}}{2}k] [0,2i]
\end{aligned}
```

此处*代表乘的意思，× 符号是叉乘,代入上面叉乘公式：$a×b=(y_az_b−y_bz_a)i+(z_ax_b−z_bx_a)j+(x_ay_b−x_by_a)k$
```math
\begin{aligned}
p′&=qp\\
&=[\frac{\sqrt{2}}{2},\frac{\sqrt{2}}{2}k] [0,2i]\\
&=[0,(2 \frac{\sqrt{2}}{2}i+2 \frac{\sqrt{2}}{2}k×i]\\
&=[0,\sqrt{2}i+\sqrt{2}j]
\end{aligned}
```
结果是一个绕了k轴转了45度的纯四元数。

我们可以确认这个四元数的向量部分的长度是不变的:

i轴: $\sqrt{2}$ ，j轴: $\sqrt{2}$ , k轴: $0$
```math
|p′|=\sqrt{\sqrt{2}^2+\sqrt{2}^2}=2
```
这正是我们所期望的！

我们可以用图像展示旋转过程：

![旋转过程](https://pic3.zhimg.com/80/v2-502c713091c336befd641bec1bd7d7d2_720w.webp)

现在，让我们考虑更一般化的四元数，即和p不正交的四元数。现在让我们把p的向量部分旋转45度：
```math
\begin{aligned}
v̂&=\frac{\sqrt{2}}{2} i+\frac{\sqrt{2}}{2}k \\
P&=2i\\
q&=[cosθ,sinθv̂]\\
p&=[0,p]
\end{aligned}
```
用向量p乘以四元数q，得到:

```math
\begin{aligned}
p′&=qp\\
&=[cosθ,sinθv̂][0,p]\\
&=[−sinθv̂⋅p,cosθp+sinθv̂×p]
\end{aligned}
```
代入单位向量v和p以及θ = 45°，我们得到：

```math
\begin{aligned}
p′&=[−\frac{\sqrt{2}}{2}(\frac{\sqrt{2}}{2}i+\frac{\sqrt{2}}{2}k)⋅(2i),\frac{\sqrt{2}}{2}2i+ （\frac{\sqrt{2}}{2}(\frac{\sqrt{2}}{2}i+\frac{\sqrt{2}}{2}k) ×（2i）] \\
&=[−1,\sqrt{2}i+j] 
\end{aligned}
```
注意，算出来的结果已经不是纯四元数了，并且，它并没有旋转45度、范数也不再是2(反而变小了，变成(√3)

)

我们可以用图像展示旋转过程：

![旋转过程](https://pic2.zhimg.com/80/v2-6543600f61c56fd7dffbc86dc9a0ed89_720w.webp)

严格来说，这样子在3维空间中表示p′ 是不正确的。因为它其实是一个4维的向量！个人认为这样标注类似于我们把三维的向量投影到二维平面上，这里是四维投影到三维上。为了简单起见，我只将这个四元数的向量部分显示出来。

然而，还有一线生机。Hamilton发现（但没有正式宣布），如果对qp右乘q的逆，出来的结果是一个纯四元数，并且四元数向量部分的范数可以保持不变。让我们试试应用在我们的例子里。

首先，让我们计算$q^−1$:
```math
q=[cosθ,sinθ(\frac{\sqrt{2}}{2}i+\frac{\sqrt{2}}{2}k)]\\
q^−1=[cosθ,−sinθ(\frac{\sqrt{2}}{2}i+\frac{\sqrt{2}}{2}k)]
```
这里$q^−1=q^∗$ 是因为$q$是单位四元数，$q^∗$为共轭四元数,q的模长等于1

```math
|q| = \cosθ^2 + \frac{2 \cosθ^2}{4} + \frac{2 \sinθ^2}{4} = 1
```
此时$q^-1$等于$q^*$。
再代入$θ=45\degree$，得到：
```math
\begin{aligned}
q^−1&=[\frac{\sqrt{2}}{2} ,−\frac{\sqrt{2}}{2}(\frac{\sqrt{2}}{2}i+ \frac{\sqrt{2}}{2}k)]\\
&=\frac{1}{2}[\sqrt{2},−i−k]
\end{aligned}
```
现在，把前面算出来的qp再次拿出来,将qp与q-1相乘得到：：
```math
\begin{aligned}
qp&=[−1,\sqrt{2}i+j]\\
qpq^−1&=[−1,\sqrt{2}i+j] * \frac{1}{2}[\sqrt{2},−i−k]  (此处代入四元数乘积一般式。点乘，叉乘公式)\\
&=\frac{1}{2}[−\sqrt{2}+ \sqrt{2}, i+k+2i+\sqrt{2}j−i+\sqrt{2}j+k]\\
&=[0,i+\sqrt{2}j+k]
\end{aligned}
```
这下是纯四元数了，并且它的范数是：

i轴: $1$，j轴: $\sqrt{2}$ , k轴: $1$
```math
|p′| = |qpq^−1|=\sqrt{1^2 + \sqrt{2}^2 + 1^2}=\sqrt{4}=2
```
这和原始的p的范数一致。

下面的图像展示了旋转结果：

![旋转结果](https://pic4.zhimg.com/80/v2-151bcbd20be7a5206d46b842b13142f3_720w.webp)

所以我们可以看到，这个结果是一个纯四元数，并且原四元数的向量的范数也保持住了。但是还有一个问题：向量被旋转了90度而不是45度。这刚好是我们需要的度数的两倍！为了正确地让一个向量绕某个轴向量旋转某个角度，我们必须以目标角度的一半来计算。因此，我们构造了下面的四元数：
```math
q=\big[cos(\frac{1}{2}θ),sin(\frac{1}{2} θ v̂)\big]
```
这就是**旋转四元数的一般形式**！

### 欧拉角转四元数：
设欧拉角 
```math
euler = (pitch,roll,yaw);
```
欧拉旋转顺序为 Z  X  Y

则每个轴转成四元数为：
```math
\begin{aligned}
q_x &= [cos(pitch/2),sin(pitch/2)i]\\
q_y &= [cos(roll /2),sin(roll/2)j]\\
q_z &= [cos(yaw /2),sin(yaw/2)k]
\end{aligned}
```
最后相乘得出结果
```math
\begin{aligned}
q &= q_x q_y q_z \\
&=[cos(yaw /2),sin(yaw/2)k] [cos(pitch/2),sin(pitch/2)i] [cos(roll /2),sin(roll/2)j]
\end{aligned}
```

### 轴角转换四元数：
四元数还可以直观用轴角表示 
```math
[x,y,z,\theta]
```
xyz代表旋转轴向量v，theta代表旋转角

则
```math
\begin{aligned}
v &= (x,y,z)\\
q &= cos(\theta/2) + sin(\theta/2)v
\end{aligned}
```
总结
四元数相比欧拉角，可以避免万向节死锁问题，其次在游戏和很多硬件等营养方面有很广泛的使用，这篇文章是我从网上看到的，本来是修复网上盲目搬运文章公式的很多错误，但是后来找到了原作者并征得同意，原作者的文章没有错误，并且有四元数线性插值部分内容，此文加上部分个人当初思考中遇到的问题和难点，原文公式比较好理解。

### 四元数转欧拉角

```math
\begin{aligned}
q &= [w, x, y, z] \\
roll &= atan2(2(wx + yz), 1 - 2(x^2 + y^2)) \\
pitch &= asin(2(wy - zx)) \\
yaw &= atan2(2(wz + xy), 1 - 2(y^2 + z^2))
\end{aligned}
```

其中，q 是四元数，roll 是绕 x 轴的旋转角度，pitch 是绕 y 轴的旋转角度，yaw 是绕 z 轴的旋转角度。

注意，这里的角度是弧度制，可以使用 math.atan2() 和 math.asin() 函数计算三角函数。