# def pytest_sessionfinish(session, exitstatus):
#     """
#     当pytest会话结束时调用此函数。
#
#     :param session: pytest会话对象，包含会话的相关信息。
#     :param exitstatus: pytest会话的退出状态码。
#     """
#     # 邮件汇总逻辑
#     if test_failures:
#         # 如果有测试用例失败，则生成包含失败用例列表的邮件内容
#         body = "以下测试用例执行失败：\n\n" + "\n".join(f"- {name}" for name in test_failures)
#         # 发送包含失败用例的邮件
#         send_test_failure_email(
#             subject="✅ 自动化测试执行完毕 - 失败汇总",
#             body=body,
#             to_emails=["1121470915@qq.com"]
#         )
#         logging.info("📬 汇总失败用例邮件已发送")
#     else:
#         # 如果所有测试用例都通过，则发送恭喜邮件
#         send_test_failure_email(
#             subject="✅ 自动化测试全部通过",
#             body="🎉 恭喜！本轮测试全部通过，无失败用例。",
#             to_emails=["1121470915@qq.com"]
#         )
#
#     # 浏览器资源清理
#     # 会话结束后，确保关闭所有打开的浏览器窗口
#     cleanup_all_drivers()
#     logging.info("✅ 所有残留浏览器已关闭")

#
# msg.attach(MIMEText(body, 'plain', 'utf-8'))
#
# # 如果提供了附件路径且文件存在，则读取附件并附加到邮件对象中
# if attachment_path and os.path.exists(attachment_path):
#     with open(attachment_path, 'rb') as f:
#         part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
#         part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
#         msg.attach(part)
#
# try:
#     # 尝试与SMTP服务器建立连接
#     with smtplib.SMTP(smtp_conf['host'], smtp_conf['port']) as server:
#         server.starttls()
#         server.login(smtp_conf['username'], smtp_conf['password'])
#
#         try:
#             # 尝试发送邮件
#             server.send_message(msg)
#             logging.info("📬 错误报告邮件发送成功 ✅")
#         except Exception as send_err:
#             # 处理邮件发送阶段可能出现的异常
#             logging.warning(f"📭 邮件发送阶段异常（可能已发送）：{send_err}")
#
# except smtplib.SMTPException as conn_err:
#     # 处理SMTP连接建立失败的异常
#     logging.error(f"❌ SMTP 建立连接失败：{conn_err}")
# except Exception as outer_err:
#     # 处理SMTP关闭阶段的其他异常，通常是无害的，可以忽略
#     logging.debug(f"🔁 SMTP 关闭阶段异常（无害，可忽略）：{outer_err}")


# """
#     pytest 会话结束时自动发送汇总邮件并附带 HTML 报告按钮。
#     """
#
#     # ✅ 生成 Allure 静态报告
#     allure_output_dir = Path("report/allure_report")
#     os.system(f"allure generate report -o {str(allure_output_dir)} --clean")
#     report_link = allure_output_dir.resolve().as_uri()  # 转为 file:/// 本地链接
#
#     # ✅ 构建 HTML 邮件内容
#     if test_failures:
#         failure_items = "".join(f"<li>{name}</li>" for name in test_failures)
#         body = f"""
#         <html>
#         <body>
#             <h2>❌ 以下测试用例执行失败：</h2>
#             <ul>{failure_items}</ul>
#             <p>📎 点击下方按钮查看详细测试报告：</p>
#             <a href="{report_link}" style="display:inline-block;padding:10px 20px;background:#dc3545;color:#fff;text-decoration:none;border-radius:5px;">查看报告</a>
#         </body>
#         </html>
#         """
#         subject = "✅ 自动化测试执行完毕 - 失败汇总"
#     else:
#         body = f"""
#         <html>
#         <body>
#             <h2>🎉 恭喜！本轮测试全部通过，无失败用例。</h2>
#             <p>📎 点击下方按钮查看完整测试报告：</p>
#             <a href="{report_link}" style="display:inline-block;padding:10px 20px;background:#28a745;color:#fff;text-decoration:none;border-radius:5px;">查看报告</a>
#         </body>
#         </html>
#         """
#         subject = "✅ 自动化测试全部通过"
#
#     # ✅ 发送 HTML 邮件（确保 send_test_failure_email 支持 html=True）
#     send_test_failure_email(
#         subject=subject,
#         body=body,
#         to_emails=["1121470915@qq.com"],
#         html=True
#     )
#
#     # ✅ 清理残留浏览器实例
#     cleanup_all_drivers()
#     logging.info("✅ 所有残留浏览器已关闭")