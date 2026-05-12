package com.manoj.edgegenai;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

public class MainActivity extends Activity {

    private WebView webView;

    static {
        try {
            System.loadLibrary("edgegenai");
        } catch (UnsatisfiedLinkError e) {
            e.printStackTrace();
        }
    }

    public native String loadModel(String modelPath);
    public native String generateText(String prompt);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webView = new WebView(this);
        setContentView(webView);

        webView.setBackgroundColor(Color.BLACK);

        WebSettings settings = webView.getSettings();

        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadsImagesAutomatically(true);
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccessFromFileURLs(true);
settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }

        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());

        webView.addJavascriptInterface(new AndroidBridge(), "AndroidBridge");

        webView.clearCache(true);
        webView.clearHistory();

webView.loadUrl("file:///android_asset/index.html?v=100");
    }

    public class AndroidBridge {

        @JavascriptInterface
        public String loadOfflineModel() {
            try {
                String modelName = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf";

                File modelFile = new File(getFilesDir(), modelName);

                if (!modelFile.exists()) {
                    InputStream input = getAssets().open("models/" + modelName);
                    FileOutputStream output = new FileOutputStream(modelFile);

                    byte[] buffer = new byte[1024 * 1024];
                    int length;

                    while ((length = input.read(buffer)) > 0) {
                        output.write(buffer, 0, length);
                    }

                    output.flush();
                    output.close();
                    input.close();
                }

                String result = loadModel(modelFile.getAbsolutePath());

                if (result == null || result.trim().isEmpty()) {
                    return "❌ Model loading failed: empty native response";
                }

                return result;

            } catch (Exception e) {
                return "❌ Model copy/load error: " + e.getMessage();
            }
        }

        @JavascriptInterface
        public String askOffline(String question) {
            try {
                if (question == null || question.trim().isEmpty()) {
                    return "❌ Please enter a question";
                }

                String result = generateText(question);

                if (result == null || result.trim().isEmpty()) {
                    return "❌ No response generated from offline model";
                }

                return result;

            } catch (Exception e) {
                return "❌ Offline model error: " + e.getMessage();
            }
        }

        @JavascriptInterface
        public void showToast(String message) {
            Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}