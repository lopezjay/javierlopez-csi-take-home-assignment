SELECT * FROM video
WHERE country IS '{COUNTRY}'
AND (
  content IS '{CONTENT}'
  OR preroll in (
    SELECT preroll FROM contentprerollpairs WHERE content IS '{CONTENT}'
  )
)
AND (
  language in (
    SELECT language FROM videos
    WHERE country IS '{COUNTRY}'
    AND (
      content IS '{CONTENT}'
      OR preroll in (
        SELECT preroll FROM contentprerollpair WHERE content IS '{CONTENT}'
      )
    )
    GROUP BY language
    HAVING count(language) > 1
  )
);