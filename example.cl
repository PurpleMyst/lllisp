(setq x (constant int 1))

(defun int twice ((int x))
  (+ x x)
)

(printf "%d\n" (twice (constant int 3)))
