# CourseHub - Buoi 4
- Migration 001: enrollment_events.
- Demo class: RACE-01, capacity = 1.
- POST /enrollments: lock class_sections bang FOR UPDATE.
- Concurrency test: 1 request 201, 1 request 409.
- Performance data: 100000 rows, dataset=performance.
- Index: idx_enrollment_events_dataset_student_time.

```text
Limit  (cost=14.56..14.57 rows=1 width=166) (actual time=0.038..0.038 rows=0 loops=1)
  Buffers: shared hit=4 dirtied=1
  ->  Sort  (cost=14.56..14.57 rows=1 width=166) (actual time=0.037..0.037 rows=0 loops=1)
        Sort Key: occurred_at DESC
        Sort Method: quicksort  Memory: 25kB
        Buffers: shared hit=4 dirtied=1
        ->  Seq Scan on enrollment_events  (cost=0.00..14.55 rows=1 width=166) (actual time=0.017..0.017 rows=0 loops=1)
              Filter: ((occurred_at >= '2025-12-20 00:00:00'::timestamp without time zone) AND ((dataset)::text = 'performance'::text) AND ((student_id)::text = '22000001'::text))
              Rows Removed by Filter: 3
              Buffers: shared hit=1 dirtied=1
Planning:
  Buffers: shared hit=8 read=3
Planning Time: 0.717 ms
Execution Time: 0.054 ms
```

```text
Limit  (cost=1.06..1.07 rows=1 width=41) (actual time=0.015..0.015 rows=0 loops=1)
  Buffers: shared hit=1
  ->  Sort  (cost=1.06..1.07 rows=1 width=41) (actual time=0.013..0.014 rows=0 loops=1)
        Sort Key: occurred_at DESC
        Sort Method: quicksort  Memory: 25kB
        Buffers: shared hit=1
        ->  Seq Scan on enrollment_events  (cost=0.00..1.05 rows=1 width=41) (actual time=0.009..0.009 rows=0 loops=1)
              Filter: ((occurred_at >= '2025-12-20 00:00:00'::timestamp without time zone) AND ((dataset)::text = 'performance'::text) AND ((student_id)::text = '22000001'::text))
              Rows Removed by Filter: 3
              Buffers: shared hit=1
Planning:
  Buffers: shared hit=49 read=1
Planning Time: 0.390 ms
Execution Time: 0.027 ms
```
