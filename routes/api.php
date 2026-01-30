<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthorController;
use App\Http\Controllers\Api\CategoryController;
use App\Http\Controllers\Api\BookController;
use App\Http\Controllers\Api\BundleController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\PromoCodeController;
use App\Http\Controllers\OrderController;

// Authentication routes (public)
Route::post('register', [AuthController::class, 'register']);
Route::post('login', [AuthController::class, 'login']);

// Protected authentication routes
Route::middleware('auth:api')->group(function () {
    Route::get('profile', [AuthController::class, 'profile']);
    Route::post('logout', [AuthController::class, 'logout']);
    Route::post('refresh', [AuthController::class, 'refresh']);
});

// Public API routes
Route::apiResource('authors', AuthorController::class);
Route::apiResource('categories', CategoryController::class);
Route::apiResource('books', BookController::class);
Route::apiResource('bundles', BundleController::class);

// Promo code validation
Route::post('validate-promo', [PromoCodeController::class, 'validateCode']);

// Orders and Checkout
Route::post('checkout', [OrderController::class, 'checkout']);
Route::get('orders/{id}', [OrderController::class, 'show']);
