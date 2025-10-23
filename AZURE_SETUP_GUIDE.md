# Azure App Service データベース接続設定ガイド

## 問題の概要

Azure App Serviceでアプリケーションのヘルスチェックが `"database":"disconnected"` を返している問題を解決します。

## 原因

Azure App Serviceでは、環境変数の設定方法が通常のローカル環境と異なります。データベース接続に必要な環境変数が正しく設定されていない可能性があります。

## 解決手順

### 1. Azure Portalでの環境変数設定

1. **Azure Portal** にログイン
2. **App Service** を選択
3. **構成** → **アプリケーション設定** をクリック
4. 以下の環境変数を追加：

| 名前 | 値 | 説明 |
|------|-----|------|
| `DB_USER` | `tech0gen10student` | データベースユーザー名 |
| `DB_PASSWORD` | `[実際のパスワード]` | データベースパスワード |
| `DB_HOST` | `rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com` | データベースホスト |
| `DB_PORT` | `3306` | データベースポート |
| `DB_NAME` | `kondo-pos` | データベース名 |

### 2. 代替設定方法（APPSETTING_プレフィックス）

Azure App Serviceでは、`APPSETTING_` プレフィックス付きの環境変数も使用できます：

| 名前 | 値 |
|------|-----|
| `APPSETTING_DB_USER` | `tech0gen10student` |
| `APPSETTING_DB_PASSWORD` | `[実際のパスワード]` |
| `APPSETTING_DB_HOST` | `rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com` |
| `APPSETTING_DB_NAME` | `kondo-pos` |

### 3. データベースファイアウォール設定の確認

1. **Azure Database for MySQL** を選択
2. **接続セキュリティ** をクリック
3. **ファイアウォール規則** で以下を確認：
   - **Azure サービスへのアクセスを許可** が有効になっている
   - または、App ServiceのIPアドレスが許可されている

### 4. SSL証明書の確認

SSL証明書 `DigiCertGlobalRootG2.crt.pem` がアプリケーションのルートディレクトリに配置されていることを確認してください。

## 設定後の確認

### 1. アプリケーションの再起動

環境変数を設定した後、App Serviceを再起動してください。

### 2. ヘルスチェックの確認

以下のURLにアクセスして接続状況を確認：
```
https://[your-app-name].azurewebsites.net/health
```

正常な場合のレスポンス：
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-23T13:53:15.613126"
}
```

### 3. ログの確認

App Serviceの **監視** → **ログストリーム** でアプリケーションログを確認し、データベース接続エラーがないかチェックしてください。

## トラブルシューティング

### よくある問題と解決方法

1. **認証エラー**
   - ユーザー名とパスワードが正しいか確認
   - データベースユーザーに適切な権限があるか確認

2. **接続エラー**
   - ファイアウォール設定を確認
   - ホスト名とポート番号が正しいか確認

3. **SSL証明書エラー**
   - SSL証明書ファイルが存在するか確認
   - 証明書ファイルのパスが正しいか確認

4. **環境変数が読み込まれない**
   - アプリケーションを再起動
   - 環境変数の名前と値が正しいか確認

## 接続テスト用スクリプト

ローカル環境で接続をテストする場合：

```bash
python test_db_connection.py
```

Azure App Service環境をテストする場合：

```bash
python azure_connection_fix.py
```

## 参考情報

- [Azure App Service のアプリケーション設定](https://docs.microsoft.com/ja-jp/azure/app-service/configure-common)
- [Azure Database for MySQL の接続セキュリティ](https://docs.microsoft.com/ja-jp/azure/mysql/concepts-security)
