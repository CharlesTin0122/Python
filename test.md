- [写在前面](#写在前面)
  - [二级标题](#二级标题)
    - [三级标题](#三级标题)
      - [四级标题](#四级标题)
# 写在前面

## 二级标题

### 三级标题

#### 四级标题

> 世上本没有路，走的人多了，也就成了路。
> — —鲁迅

```python
import pymel.core as pm

print(pm)
```

* red
* blue
* green

-[ ] asdasdsadsada
-[ ] asfasgdfghsdfhgsf

$(x^2 + x^y )^{x^y}+ x_1^2= y_1 - y_2^{x_1-y_1^2}$

$\vec a \cdot \vec b = 1$

$ \pm \times \div \mid $

```Python
import pymel.core as pm
pm.setAttr()
```


Quaternion Interpolation
One of the most important reasons for using quaternions in computer graphics is that quaternions are very good at representing rotations in space. Quaternions overcome the issues that plague other methods of rotating points in 3D space such as Gimbal lock which is an issue when you represent your rotation with euler angles.

Using quaternions, we can define several methods that represents a rotational interpolation in 3D space. The first method I will examine is called SLERP which is used to smoothly interpolate a point between two orientations. The second method is an extension of SLERP called SQAD which is used to interpolate through a sequence of orientations that define a path.

SLERP
SLERP stands for Spherical Linear Interpolation. SLERP provides a method to smoothly interpolate a point about two orientations.

I will represent the first orientation as q1
 and the second orientation as q2
. The point that is interpolated will be represented by p
 and the interpolated point will be represented by p′
. The interpolation parameter t
 will interpolate p
 from q1
 when t=0
 to q2
 when t=1
.

The standard linear interpolation formula is:

p′=p1+t(p2−p1)
The general steps to apply this equation are:

Compute the difference between p1
 and p2
.
Take the fractional part of that difference.
Adjust the original value by the fractional difference between the two points.
We can use the same basic principle to interpolate between two quaternion orientations.

QUATERNION DIFFERENCE
The first step dictates that we must compute the difference between q1
 and q2
. With regards to quaternions, this is equivalent to computing the angular difference between the two quaternions.

Δq=q−11q2
QUATERNION EXPONENTIATION
The next step is to take the fractional part of that difference. We can compute the fractional part of a quaternion by raising it to a power whose value is in the range [0…1]
.

The general formula for quaternion exponentiation is:

qt=exp(tlogq)
Where the exponential function for quaternions is given by:

exp(q)==exp([0,θv^])[cosθ,sinθv^]
And the logarithm of a quaternion is given by:

logq====log(cosθ+sinθv^)log(exp(θv^))θv^[0,θv^]
For t=0
, we have:

q0====exp(0logq)exp([cos(0),sin(0)v^])exp([1,0])[1,0]
And for t=1
, we have:

q1==exp(logq)q
FRACTIONAL DIFFERENCE OF QUATERNIONS
To compute the interpolated angular rotation, we adjust the original orientation q1
 by the fractional part of the difference between q1
 and q2
.

q′=q1(q−11q2)t
Which is the general form of spherical linear interpolation using quaternions. However, this is not the form of the SLERP equation that is commonly used in practice.

We can apply a similar formula for performing a spherical interpolation of vectors to quaternions. The general form of a spherical interpolation for vectors is defined as:

vt=sin(1−t)θsinθv1+sintθsinθv2
This is visualized in the following image.

Quaternion Interpolation
Quaternion Interpolation

This formula can be applied unmodified to quaternions:

qt=sin(1−t)θsinθq1+sintθsinθq2
And we can obtain the angle θ
 by computing the dot-product between q1
 and q2
.

cosθθ===q1⋅q2|q1||q2|s1s2+x1x2+y1y2+z1z2|q1||q2|cos−1(s1s2+x1x2+y1y2+z1z2|q1||q2|)
CONSIDERATIONS
There are two issues with this implementation which must be taken into consideration during implementation.

First, if the quaternion dot-product results in a negative value, then the resulting interpolation will travel the “long-way” around the 4D sphere which is not necessarily what we want. To solve this problem, we can test the result of the dot product and if it is negative, then we can negate one of the orientations. Negating the scalar and the vector part of the quaternion does not change the orientation that it represents but by doing this we guarantee that the rotation will be applied in the “shortest” path.

The other problem arises when the angular difference between q1
 and q2
 is very small then sinθ
 becomes 0. If this happens, then we will get an undefined result when we divide by sinθ
. In this case, we can fall-back to using linear interpolation between q1
 and q2
.

SQUAD
Just as a SLERP can be used to compute an interpolation between two quaternions, a SQUAD (Spherical and Quadrangle) can be used to smoothly interpolate over a path of rotations.

If we have the sequence of quaternions:

q1,q2,q3,⋯,qn−2,qn−1,qn
And we also define the “helper” quaternion (si
) which we can consider an intermediate control point:

si=exp(−log(qi+1q−1i)+log(qi−1q−1i)4)qi
Then the orientation along the sub-cuve defined by:

qi−1,qi,qi+1,qi+2
at time t is given by:

squad(qi,qi+1,si,si+1,t)=slerp(slerp(qi,qi+1,t),slerp(si,si+1,t),2t(1−t))
Conclusion
Despite being extremely difficult to understand, quaternions provide a few obvious advantages over using matrices or Euler angles for representing rotations.

Quaternion interpolation using SLERP and SQUAD provide a way to interpolate smoothly between orientations in space.
Rotation concatenation using quaternions is faster than combining rotations expressed in matrix form.
For unit-norm quaternions, the inverse of the rotation is taken by subtracting the vector part of the quaternion. Computing the inverse of a rotation matrix is considerably slower if the matrix is not orthonormalized (if it is, then it’s just the transpose of the matrix).
Converting quaternions to matrices is slightly faster than for Euler angles.
Quaternions only require 4 numbers (3 if they are normalized. The Real part can be computed at run-time) to represent a rotation where a matrix requires at least 9 values.
However for all of the advantages in favor of using quaternions, there are also a few disadvantages.

Quaternions can become invalid because of floating-point round-off error however this “error creep” can be resolved by re-normalizing the quaternion.
And probably the most significant deterrent for using quaternions is that they are very hard to understand. I hope that this issue is resolved after reading this article.
There are several math libraries that implement quaternions and a few of those libraries implement quaternions correctly. In my personal experience, I find GLM (OpenGL Math Library) to be a good math library with a good implementation of quaternions. If you are interested in using quaternions in your own applications, this is the library I would recommend.

Download the Demo
I created a small demo that demonstrates how a quaternion is used to rotate an object in space. The demo was created with Unity 3.5.2 which you can download for free and view the demo script files. The zip file also contains a Windows binary executable but Using Unity, you can also generate a Mac application (and Unity 4 introduces Linux builds as well).