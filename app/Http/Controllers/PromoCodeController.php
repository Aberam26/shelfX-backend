<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;

class PromoCodeController extends Controller
{
    // Example promo codes
    private $codes = [
        'SAVE10' => 10, // 10% discount
        'BOOK5' => 5,   // 5% discount
        'WELCOME20' => 20, // 20% discount
        'FREESHIP' => 100, // 100% discount (for testing)
        'SUMMER15' => 15, // 15% discount
        'EXTRA25' => 25, // 25% discount
        'READMORE' => 12, // 12% discount
    ];

    public function validateCode(Request $request)
    {
        // Accept both form-data and JSON
        $code = $request->input('code');
        if (!$code && $request->isJson()) {
            $data = $request->json()->all();
            $code = isset($data['code']) ? $data['code'] : null;
        }
        $code = strtoupper($code);
        if (isset($this->codes[$code])) {
            return response()->json([
                'valid' => true,
                'discount' => $this->codes[$code],
            ]);
        }
        return response()->json([
            'valid' => false,
            'discount' => 0,
        ]);
    }
}
