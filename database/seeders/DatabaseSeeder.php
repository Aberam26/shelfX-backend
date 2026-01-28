<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Author;
use App\Models\Category;
use App\Models\Book;
use App\Models\Bundle;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // Seed Categories
        $categories = [
            ['name' => 'Children', 'slug' => 'children', 'description' => 'Books for young readers'],
            ['name' => 'Fantasy', 'slug' => 'fantasy', 'description' => 'Magical worlds and epic adventures'],
            ['name' => 'Thriller', 'slug' => 'thriller', 'description' => 'Suspense and mystery'],
            ['name' => 'Ancient', 'slug' => 'ancient', 'description' => 'Historical and classical literature'],
            ['name' => 'Romance', 'slug' => 'romance', 'description' => 'Love stories and relationships'],
            ['name' => 'Science Fiction', 'slug' => 'sci-fi', 'description' => 'Future worlds and technology'],
            ['name' => 'Biography', 'slug' => 'biography', 'description' => 'Life stories of remarkable people'],
            ['name' => 'Self-Help', 'slug' => 'self-help', 'description' => 'Personal development and growth'],
        ];

        foreach ($categories as $category) {
            Category::create($category);
        }

        // Seed Authors
        $authors = [
            ['name' => 'J.K. Rowling', 'bio' => 'British author best known for the Harry Potter series', 'image' => 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200'],
            ['name' => 'Stephen King', 'bio' => 'American author of horror, supernatural fiction', 'image' => 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200'],
            ['name' => 'Agatha Christie', 'bio' => 'British writer known for detective novels', 'image' => 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200'],
            ['name' => 'George R.R. Martin', 'bio' => 'American novelist and short story writer', 'image' => 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200'],
            ['name' => 'Jane Austen', 'bio' => 'English novelist known for romantic fiction', 'image' => 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200'],
            ['name' => 'Isaac Asimov', 'bio' => 'American author and professor of biochemistry', 'image' => 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200'],
        ];

        foreach ($authors as $author) {
            Author::create($author);
        }

        // Seed Books
        $books = [
            [
                'title' => 'The Midnight Library',
                'author_id' => 1,
                'category_id' => 2,
                'price' => 18.99,
                'original_price' => 24.99,
                'cover' => 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
                'description' => 'Between life and death there is a library, and within that library, the shelves go on forever.',
                'stock' => 45,
                'rating' => 4.8,
                'review_count' => 2341,
                'sales_count' => 15420,
                'view_count' => 45000,
                'isbn' => '978-0-525-55947-4',
                'pages' => 304,
                'publisher' => 'Viking',
                'language' => 'English'
            ],
            [
                'title' => 'The Silent Patient',
                'author_id' => 3,
                'category_id' => 3,
                'price' => 16.99,
                'cover' => 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400',
                'description' => 'A shocking psychological thriller of a woman\'s act of violence against her husband.',
                'stock' => 32,
                'rating' => 4.6,
                'review_count' => 1892,
                'sales_count' => 12300,
                'view_count' => 38000,
                'isbn' => '978-1-250-30169-7',
                'pages' => 336,
                'publisher' => 'Celadon Books',
                'language' => 'English'
            ],
            [
                'title' => 'Where the Wild Things Are',
                'author_id' => 1,
                'category_id' => 1,
                'price' => 12.99,
                'original_price' => 15.99,
                'cover' => 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400',
                'description' => 'A timeless classic about imagination and the wild things within us all.',
                'stock' => 78,
                'rating' => 4.9,
                'review_count' => 5621,
                'sales_count' => 28000,
                'view_count' => 62000,
                'isbn' => '978-0-06-025492-6',
                'pages' => 48,
                'publisher' => 'Harper Collins',
                'language' => 'English'
            ],
            [
                'title' => 'A Game of Thrones',
                'author_id' => 4,
                'category_id' => 2,
                'price' => 22.99,
                'cover' => 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400',
                'description' => 'Winter is coming. The epic fantasy that started it all.',
                'stock' => 0,
                'rating' => 4.7,
                'review_count' => 8934,
                'sales_count' => 45000,
                'view_count' => 120000,
                'isbn' => '978-0-553-10354-0',
                'pages' => 694,
                'publisher' => 'Bantam Books',
                'language' => 'English'
            ],
            [
                'title' => 'Pride and Prejudice',
                'author_id' => 5,
                'category_id' => 5,
                'price' => 11.99,
                'cover' => 'https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=400',
                'description' => 'The classic tale of love and misunderstanding in Georgian England.',
                'stock' => 56,
                'rating' => 4.8,
                'review_count' => 12500,
                'sales_count' => 52000,
                'view_count' => 98000,
                'isbn' => '978-0-14-143951-8',
                'pages' => 432,
                'publisher' => 'Penguin Classics',
                'language' => 'English'
            ],
            [
                'title' => 'Foundation',
                'author_id' => 6,
                'category_id' => 6,
                'price' => 15.99,
                'original_price' => 19.99,
                'cover' => 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400',
                'description' => 'The epic saga of the Foundation that spans the galaxy.',
                'stock' => 23,
                'rating' => 4.5,
                'review_count' => 3421,
                'sales_count' => 18000,
                'view_count' => 42000,
                'isbn' => '978-0-553-29335-7',
                'pages' => 255,
                'publisher' => 'Bantam Spectra',
                'language' => 'English'
            ],
            [
                'title' => 'The Shining',
                'author_id' => 2,
                'category_id' => 3,
                'price' => 14.99,
                'cover' => 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400',
                'description' => 'A masterpiece of modern horror from the king of the genre.',
                'stock' => 41,
                'rating' => 4.6,
                'review_count' => 6789,
                'sales_count' => 32000,
                'view_count' => 78000,
                'isbn' => '978-0-307-74365-1',
                'pages' => 447,
                'publisher' => 'Anchor',
                'language' => 'English'
            ],
            [
                'title' => 'Murder on the Orient Express',
                'author_id' => 3,
                'category_id' => 3,
                'price' => 13.99,
                'original_price' => 16.99,
                'cover' => 'https://images.unsplash.com/photo-1509266272358-7701da638078?w=400',
                'description' => 'Hercule Poirot\'s most famous case aboard the legendary train.',
                'stock' => 5,
                'rating' => 4.7,
                'review_count' => 4532,
                'sales_count' => 25000,
                'view_count' => 55000,
                'isbn' => '978-0-06-269366-2',
                'pages' => 256,
                'publisher' => 'William Morrow',
                'language' => 'English'
            ],
        ];

        foreach ($books as $book) {
            Book::create($book);
        }

        // Seed Bundles
        $bundle1 = Bundle::create([
            'name' => 'Mystery Lovers Collection',
            'description' => 'Three bestselling thrillers that will keep you on the edge of your seat',
            'price' => 39.99,
            'original_price' => 45.97,
            'image' => 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=600'
        ]);
        $bundle1->books()->attach([2, 7, 8]);

        $bundle2 = Bundle::create([
            'name' => 'Fantasy Epic Bundle',
            'description' => 'Escape to magical worlds with these fantasy favorites',
            'price' => 36.99,
            'original_price' => 47.98,
            'image' => 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=600'
        ]);
        $bundle2->books()->attach([1, 4]);
    }
}
