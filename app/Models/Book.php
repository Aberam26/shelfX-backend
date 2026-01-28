<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Book extends Model
{
    protected $fillable = [
        'title',
        'author_id',
        'category_id',
        'price',
        'original_price',
        'cover',
        'description',
        'stock',
        'rating',
        'review_count',
        'sales_count',
        'view_count',
        'isbn',
        'pages',
        'publisher',
        'language',
    ];

    protected $casts = [
        'price' => 'decimal:2',
        'original_price' => 'decimal:2',
        'rating' => 'decimal:2',
    ];

    /**
     * Get the author that owns the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the category that owns the book.
     */
    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    /**
     * The bundles that belong to the book.
     */
    public function bundles(): BelongsToMany
    {
        return $this->belongsToMany(Bundle::class);
    }
}
