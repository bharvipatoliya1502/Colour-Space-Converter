# Validation Results

Date: 2026-11-27T03:08:12+05:30
Python: 3.13.18
NumPy: 2.5.3
Pillow: 12.3.0
Streamlit: 1.67.0
Matplotlib: 3.11.2

## Pytest result

`Summary unavailable`

## Passed tests

- `tests/test_app_smoke.py::test_app_smoke_has_five_tabs_without_exception PASSED [  1%]`
- `tests/test_batch_processor.py::TestBatchProcessor::test_corrupt_image_is_saved_as_failed PASSED [  3%]`
- `tests/test_batch_processor.py::TestBatchProcessor::test_valid_image_is_processed_and_saved_as_success PASSED [  5%]`
- `tests/test_batch_processor_jobs.py::test_enqueue_creates_queued_job_and_run_success PASSED [  7%]`
- `tests/test_batch_processor_jobs.py::test_corrupt_batch_job_is_failed PASSED [  9%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_determinant_matches_numpy PASSED [ 10%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_determinant_normal PASSED [ 12%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_determinant_singular_edge PASSED [ 14%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_inverse_matches_numpy PASSED [ 16%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_inverse_normal PASSED [ 18%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_inverse_singular_edge PASSED [ 20%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_matrix_multiply_dimension_error PASSED [ 21%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_matrix_multiply_matches_numpy PASSED [ 23%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_matrix_multiply_normal PASSED [ 25%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_rank_matches_numpy PASSED [ 27%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_rank_normal PASSED   [ 29%]`
- `tests/test_converter.py::TestMatrixAlgorithms::test_rank_zero_edge PASSED [ 30%]`
- `tests/test_converter.py::TestColourConversion::test_grayscale_shape_and_rank PASSED [ 32%]`
- `tests/test_converter.py::TestColourConversion::test_image_round_trip PASSED [ 34%]`
- `tests/test_converter.py::TestColourConversion::test_known_pixel PASSED   [ 36%]`
- `tests/test_converter.py::TestColourConversion::test_pixel_round_trip_edge_black PASSED [ 38%]`
- `tests/test_converter.py::TestColourConversion::test_rgb_yiq_matrix_matches_numpy PASSED [ 40%]`
- `tests/test_converter.py::TestQueue::test_empty_queue PASSED              [ 41%]`
- `tests/test_converter.py::TestQueue::test_fifo_order PASSED               [ 43%]`
- `tests/test_database.py::TestDatabasePersistence::test_failed_batch_job_is_persisted PASSED [ 45%]`
- `tests/test_database.py::TestDatabasePersistence::test_image_dimensions_can_be_updated_after_decode PASSED [ 47%]`
- `tests/test_database.py::TestDatabasePersistence::test_successful_conversion_is_readable_from_database PASSED [ 49%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_change_of_basis_matches_numpy_reference PASSED [ 50%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_change_of_basis_rejects_invalid_vector PASSED [ 52%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_change_of_basis_round_trip PASSED [ 54%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_grayscale_edge_black_and_white PASSED [ 56%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_grayscale_matches_numpy_reference PASSED [ 58%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_grayscale_normal PASSED [ 60%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_image_difference_edge_identical_images PASSED [ 61%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_image_difference_matches_numpy_reference PASSED [ 63%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_image_difference_rejects_mismatched_dimensions PASSED [ 65%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_inverse_image_edge_rejects_wrong_shape PASSED [ 67%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_inverse_image_matches_independent_numpy_calculation PASSED [ 69%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_inverse_image_normal_round_trip PASSED [ 70%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_rgb_to_yiq_image_edge_single_pixel_black_and_white PASSED [ 72%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_rgb_to_yiq_image_matches_numpy_library PASSED [ 74%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_rgb_to_yiq_image_normal PASSED [ 76%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_yiq_to_rgb_pixel_edge_white PASSED [ 78%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_yiq_to_rgb_pixel_matches_numpy PASSED [ 80%]`
- `tests/test_image_conversion.py::TestImageConversionValidation::test_yiq_to_rgb_pixel_normal PASSED [ 81%]`
- `tests/test_linear_algebra_extensions.py::test_nullspace_grayscale_basis PASSED [ 83%]`
- `tests/test_linear_algebra_extensions.py::test_nullspace_full_rank_empty PASSED [ 85%]`
- `tests/test_linear_algebra_extensions.py::test_nullspace_zero_matrix_standard_basis_and_numpy PASSED [ 87%]`
- `tests/test_linear_algebra_extensions.py::test_nullspace_numpy_dimension PASSED [ 89%]`
- `tests/test_linear_algebra_extensions.py::test_projection_idempotent_and_rank PASSED [ 90%]`
- `tests/test_linear_algebra_extensions.py::test_same_gray_demo_valid PASSED [ 92%]`
- `tests/test_linear_algebra_extensions.py::test_grayscale_pixel_matrix_path PASSED [ 94%]`
- `tests/test_linear_algebra_extensions.py::test_grayscale_null_space_api_returns_two_valid_vectors PASSED [ 96%]`
- `tests/test_linear_algebra_extensions.py::test_same_gray_demo_edge_colour_and_numpy_gray_reference PASSED [ 98%]`
- `tests/test_plots.py::test_histogram_returns_three_axes PASSED            [100%]`

## From-scratch vs NumPy comparison

| Check | Maximum absolute difference |
|---|---:|
| Sample pixel (255,120,60) to YIQ | 1.421e-14 |
| Determinant | 1.110e-16 |
| Inverse matrix | 2.220e-16 |
| Rank | 0.000e+00 |
| Null-space check ||Gv|| | 0.000e+00 |
