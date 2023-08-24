- [上下标](#上下标)
- [括号](#括号)
- [增大括号](#增大括号)
- [其他的大括号](#其他的大括号)
- [分数](#分数)
- [开方](#开方)
- [累加/累乘](#累加累乘)
- [三角函数](#三角函数)
- [对数函数](#对数函数)
- [二元运算符](#二元运算符)
- [关系符号](#关系符号)
- [极限](#极限)
- [向量](#向量)
- [箭头](#箭头)
- [集合](#集合)
- [微积分](#微积分)
- [希腊字母](#希腊字母)
- [空格](#空格)
- [矩阵](#矩阵)
# 上下标

$$a_0, a_{pre}$$
$$a^0, a^{[0]}$$

# 括号
$$
(, )
[, ]
\lang, \rang
$$

# 增大括号
$$
(x)
\big( x \big)
\Big( x \Big)
\bigg( x \bigg)
\bigg( x \bigg)
$$

# 其他的大括号

$$
\Bigg(\bigg(\Big(\big((x)\big)\Big)\bigg)\Bigg)
\Bigg[\bigg[\Big[\big[[x]\big]\Big]\bigg]\Bigg]
\Bigg[\bigg[\Big[\big[[x]\big]\Big]\bigg]\Bigg]
\Bigg\lvert\bigg\lvert\Big\lvert\big\lvert\lvert x \rvert\big\rvert\Big\rvert\bigg\rvert\Bigg\rvert
\Bigg\lVert\bigg\lVert\Big\lVert\big\lVert\lVert x \rVert\big\rVert\Big\rVert\bigg\rVert\Bigg\rVert
\Bigg\lVert\bigg\lVert\Big\lVert\big\lVert\lVert x \rVert\big\rVert\Big\rVert\bigg\rVert\Bigg\rVert
$$

# 分数
$$
\frac{a}{b}
$$

# 开方
$$
\sqrt{a + b},
\sqrt[n]{a + b}
$$

# 累加/累乘

$$
\sum_{i = 0}{n}\frac{1}{i^2}
$$
$$
\prod_{i = 0}{n}\frac{1}{x^2}
$$

# 三角函数
$$
\sin(x), \cos(x), \tan(x), \cot(x), \sec(x), \csc(x),\bot,\angle,40^\circ
$$

# 对数函数
$$
\ln{a + b}, \log_{a}^{b}, \lg{a + b}
$$

# 二元运算符
$$
\pm, \mp, \times, \div, \ast, \mid
$$

# 关系符号
$$
\leq, \geq, \equiv, 
$$

# 极限
$$
\lim_{x \to 0}, \lim_{x \to \infty},
\lim, \rightarrow, \infty,
\lim_{n\rightarrow+\infty}n
$$

# 向量
$$
\vec{a}, \vec{b}, \vec{c}
$$

# 箭头
$$
\rightarrow, \leftarrow, \leftrightarrow, \uparrow, \downarrow, \updownarrow
$$

# 集合
$$
\emptyset,
\in,
\ni,
\notin,
\subset,
\supset,
\not\subset ,
\subseteq,
\supseteq,
\cup,
\bigcup,
\cap,
\bigcap,
\uplus,
\biguplus,
\sqsubset,
\sqsupset,
\sqcap,
\sqsubseteq,
\sqsupseteq,
\vee,
\wedge,
\setminus
$$

# 微积分
$$
\prime,
\int,
\iint,
\iiint,
\oint,
\nabla,
\int_0^2 x^2 dx
$$

# 希腊字母
$$
\Alpha, \alpha,
\Beta, \beta,
\Gamma, \gamma,
\Delta, \delta,
\Epsilon, \epsilon,
\varepsilon,
\Zeta, \zeta,
\Eta, \eta,
\Theta, \theta,
\Iota, \iota,
\Kappa, \kappa,
\Lambda, \lambda,
\Mu, \mu,
\Nu, \nu,
\Xi, \xi,
\Omicron, \omicron,
\Pi, \pi,
\Rho, \rho,
\Sigma, \sigma,
\Tau, \tau,
\Upsilon, \upsilon,
\Phi, \phi,
\varphi,
\Chi, \chi,
\Psi, \psi,
\Omega, \omega
$$

# 空格
$$
123\quad123,
123\qquad123
$$

# 矩阵
$$
\begin{matrix}
1 & 2 & 3\\
4 & 5 & 6 \\
7 & 8 & 9
\end{matrix}
\tag{1}
$$

$$\left(
\begin{matrix}
1 & 2 & 3\\
4 & 5 & 6 \\
7 & 8 & 9
\end{matrix}
\right)
\tag{2}
$$

$$\left[
\begin{matrix}
1 & 2 & 3\\
4 & 5 & 6 \\
7 & 8 & 9
\end{matrix}
\right]
\tag{3}
$$

$$\left\{
\begin{matrix}
1 & 2 & 3\\
4 & 5 & 6 \\
7 & 8 & 9
\end{matrix}
\right\}
\tag{4}
$$

$$
\left[
\begin{matrix}
a & b & \cdots & a\\
b & b & \cdots & b\\
\vdots & \vdots & \ddots & \vdots\\
c & c & \cdots & c
\end{matrix}
\right]
\tag{5}
$$

$$
\left[
\begin{array}{c|cc}
1 & 2 & 3 \\
4 & 5 & 6 \\
7 & 8 & 9
\end{array}
\right]
\tag{6}
$$

$$
\left[
    \begin{array}{c|cc}
    1 & 2 & 3 \\ \hline
    4 & 5 & 6 \\
    7 & 8 & 9
    \end{array}
\right]
\tag{7}
$$


```python
import pymel.core as pm
pm.polyCube()
```