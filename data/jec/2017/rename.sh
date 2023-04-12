for f in ./*\.txt*; do
    mv -n "$f" "${f%%\.txt*}"
done
