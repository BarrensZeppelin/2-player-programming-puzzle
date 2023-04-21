# CHECKPOINT 1

The next objective is to retrieve the passphrase for decryption:
`mcrypt -d task2.md.nc`

Define:
$$
 x_0 = 0 \\
 A = <A> \\
 B = <B> \\
 C = <C> \\
 x_i = (x_{i-1} \cdot A + B) \mod C \\
 y_i = x_i \mod 26
$$

The passphrase is the concatenation of the lowercase letters corresponding to $y_1, y_2, \ldots, y_8$.
