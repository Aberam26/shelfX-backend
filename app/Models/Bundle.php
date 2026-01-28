<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Bundle extends Model
{
    protected $fillable = [
        'name',
        'description',
        'price',
        'original_price',
        'image',
    ];

    protected $casts = [
        'price' => 'decimal:2',
        'original_price' => 'decimal:2',
    ];

    /**
     * The books that belong to the bundle.
     */
    public function books(): BelongsToMany
    {
        return $this->belongsToMany(Book::class);
    }
}
