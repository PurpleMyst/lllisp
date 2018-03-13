(setq x (constant int 1))

(defun void countdown ((int x))
  (if (not (= x (constant int 0)))
    (progn
      (printf "%d\n" x)
      (recur (+ x (constant int -1))))))

(countdown (constant int 3))
