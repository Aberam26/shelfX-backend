<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Bundle;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class BundleController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index(): JsonResponse
    {
        $bundles = Bundle::with('books.author')->get();
        return response()->json($bundles);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'description' => 'required|string',
            'price' => 'required|numeric|min:0',
            'original_price' => 'required|numeric|min:0',
            'image' => 'required|string',
            'book_ids' => 'required|array',
            'book_ids.*' => 'exists:books,id',
        ]);

        $bundle = Bundle::create($validated);
        $bundle->books()->attach($validated['book_ids']);
        $bundle->load('books');
        
        return response()->json($bundle, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id): JsonResponse
    {
        $bundle = Bundle::with('books.author', 'books.category')->findOrFail($id);
        return response()->json($bundle);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id): JsonResponse
    {
        $bundle = Bundle::findOrFail($id);
        
        $validated = $request->validate([
            'name' => 'sometimes|string|max:255',
            'description' => 'sometimes|string',
            'price' => 'sometimes|numeric|min:0',
            'original_price' => 'sometimes|numeric|min:0',
            'image' => 'sometimes|string',
            'book_ids' => 'sometimes|array',
            'book_ids.*' => 'exists:books,id',
        ]);

        $bundle->update($validated);
        
        if (isset($validated['book_ids'])) {
            $bundle->books()->sync($validated['book_ids']);
        }
        
        $bundle->load('books');
        return response()->json($bundle);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id): JsonResponse
    {
        $bundle = Bundle::findOrFail($id);
        $bundle->delete();
        return response()->json(['message' => 'Bundle deleted successfully']);
    }
}
