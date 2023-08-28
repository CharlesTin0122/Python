# 四元数描述旋转
![avatar](https://img-blog.csdnimg.cn/40010053554f4d87bd03e681a412206e.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA6LCi6bG8,size_20,color_FFFFFF,t_70,g_se,x_16)
## 提问

三维空间中，假设有一个点P = (x, y, z) 和一个向量 V = (v1, v2, v3)，将 P 绕着 V 旋转θ（弧度）得到的结果是新的点 P' = (x', y', z')。请用四元数计算P'，并给出详细的计算过程。

## 计算

在三维空间中，使用四元数来表示旋转是一种有效的方法。四元数可以用来表示旋转轴和旋转角度，从而实现点的旋转操作。

### 1.旋转轴向量V转化为单位向量
首先，我们需要将旋转向量V单位化，然后构造四元数来表示旋转。假设单位化后的旋转向量为 
$$
U = \frac{V}{|V|} = (u_1, u_2, u_3)
$$

### 2.构造旋转四元数
四元数的表示为 
$$
q = \cos(θ/2) + (u_1 * i + u_2 * j + u_3 * k) * \sin(θ/2)
$$
此四元数包含了旋转轴向和旋转角度的信息， 其中i、j、k 是虚部单位向量，θ 是旋转角度。

### 3.构造四元数共轭
四元数的共轭为 
$$
q_conj = \cos(θ/2) - (u_1 * i + u_2 * j + u_3 * k) * \sin(θ/2)
$$

### 4.将点P转换为四元数表示
将点P表示为四元数 
$$
P = x * i + y * j + z * k
$$

### 5.实现旋转
然后，我们可以通过四元数的乘法来实现点P的旋转：

P' = q * P * q_conj

其中 q是旋转四元数，P 是点P的四元数表示，q_conj 是四元数q的共轭。

## 详细的计算过程：

计算 q * P * q_conj：

### 首先
计算 P * q_conj，得到旋转回原始坐标系的点：

P_rotated = P * q_conj

```math
\begin{array}{l}
P \underline{-} rotated = (x * i + y * j + z * k) * (cos(θ/2) - (u1 * i + u2 * j + u3 * k) * sin(θ/2))\\

= x * cos(θ/2) * i + y * cos(θ/2) * j + z * cos(θ/2) * k

(x * u1 + y * u2 + z * u3) * sin(θ/2) * i
(x * u1 + y * u2 + z * u3) * sin(θ/2) * j
(x * u1 + y * u2 + z * u3) * sin(θ/2) * k  \\
= (x * cos(θ/2) - (x * u1 + y * u2 + z * u3) * sin(θ/2)) * i

(y * cos(θ/2) - (x * u1 + y * u2 + z * u3) * sin(θ/2)) * j
(z * cos(θ/2) - (x * u1 + y * u2 + z * u3) * sin(θ/2)) * k  \\
= (x * cos(θ/2) - dot(P, U) * sin(θ/2)) * i
(y * cos(θ/2) - dot(P, U) * sin(θ/2)) * j
(z * cos(θ/2) - dot(P, U) * sin(θ/2)) * k
\end{array}
```

其中，dot(P, U) = x * u1 + y * u2 + z * u3 是点 P 在单位旋转向量 U 上的投影。


### 然后
计算 q * P_rotated，得到旋转后的点的四元数表示：

P_final = q * P_rotated
```math
\begin{array}{l}
P\underline{-}final = (cos(θ/2) + (u1 * i + u2 * j + u3 * k) * sin(θ/2)) * (x_rotated * i + y_rotated * j + z_rotated * k)\\
= cos(θ/2) * x_rotated * i + cos(θ/2) * y_rotated * j + cos(θ/2) * z_rotated * k

(u1 * i + u2 * j + u3 * k) * sin(θ/2) * x_rotated * i
(u1 * i + u2 * j + u3 * k) * sin(θ/2) * y_rotated * j
(u1 * i + u2 * j + u3 * k) * sin(θ/2) * z_rotated * k\\
= (cos(θ/2) * x_rotated + u1 * sin(θ/2) * x_rotated) * i
(cos(θ/2) * y_rotated + u2 * sin(θ/2) * y_rotated) * j
(cos(θ/2) * z_rotated + u3 * sin(θ/2) * z_rotated) * k\\
= ((cos(θ/2) + u1 * sin(θ/2)) * x_rotated) * i
((cos(θ/2) + u2 * sin(θ/2)) * y_rotated) * j
((cos(θ/2) + u3 * sin(θ/2)) * z_rotated) * k\\
= x_final * i + y_final * j + z_final * k
\end{array}
```
其中，x_final、y_final、z_final 是旋转后点 P_final 的坐标。

### 最后
提取旋转后的点 P' 的坐标，即从 P_final 中提取 x'、y'、z'。

## 总结

计算单位化旋转向量 U。
构造四元数 q。
将点 P 转换为四元数表示。
计算四元数的共轭 q_conj。
计算旋转后的四元数 P' = q * P * q_conj。
提取旋转后的坐标 x', y', z'。
这个过程使用了四元数的性质，可以更高效地进行旋转操作，尤其在连续的旋转操作中。


## Python 代码计算
```Python
import numpy as np

def quaternion_rotation(point, axis, angle):
    """
    使用四元数使点point绕axis轴旋转angle弧度后得到点point的新坐标

    Args:
        point (numpy.ndarray): 要被旋转的点坐标.
        axis (numpy.ndarray): 旋转轴向量.
        angle (float): 旋转弧度.

    Returns:
        numpy.ndarray: 旋转后的点坐标.
    """
    # 步骤1：将轴向量单位化
    axis = axis / np.linalg.norm(axis)

    # 步骤2：计算四元数
    w = np.cos(angle/2)
    v = axis * np.sin(angle/2)
    quaternion = np.array([w, *v])

    # 步骤3：将点转换为四元数表示
    p = np.array([0, *point])

    # 步骤4：旋转点
    p_rotated = quaternion_multiply(quaternion_multiply(quaternion, p), quaternion_inverse(quaternion))

    # 步骤5：提取旋转后的坐标
    point_rotated = p_rotated[1:]

    return point_rotated

# Example usage
point = np.array([x, y, z])
axis = np.array([v1, v2, v3])
angle = theta

point_rotated = quaternion_rotation(point, axis, angle)
print("旋转后的点：", point_rotated)
```
$$
\sin(\theta/2)
$$