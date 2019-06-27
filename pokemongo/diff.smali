.method private locationUpdate(Landroid/location/Location;[I)V
    .locals 8
    .param p1, "location"    # Landroid/location/Location;
    .param p2, "status"    # [I

    .prologue
    .line 200
    iget-object v1, p0, Lcom/nianticlabs/nia/location/NianticLocationManager;->callbackLock:Ljava/lang/Object;

    monitor-enter v1

    .line 201
    :try_start_0
    iget-object v0, p0, Lcom/nianticlabs/nia/location/NianticLocationManager;->context:Landroid/content/Context;

    # ===================
    # Inserted code start
    # ===================

    :insert_start_0

    if-eqz p1, :cond_0

    # v3 = v0.getExternalFilesDir(null)
    const/4 v3, 0x0
    invoke-virtual {v0, v3}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;
    move-result-object v3

    # v4 = "location"
    const-string v4, "location"

    # v2 = new File(v3, "location")
    new-instance v2, Ljava/io/File;
    invoke-direct {v2, v3, v4}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V

    # if v2.isFile()
    invoke-virtual {v2}, Ljava/io/File;->isFile()Z
    move-result v3

    if-eqz v3, :cond_0

    # v3 = new FileInputStream(v2)
    new-instance v3, Ljava/io/FileInputStream;
    invoke-direct {v3, v2}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    # v6 = 256
    const/16 v6, 0x100

    # v6 = new byte[256]
    new-array v6, v6, [B

    # v3.read(v6)
    invoke-virtual {v3, v6}, Ljava/io/FileInputStream;->read([B)I

    # v3.close()
    invoke-virtual {v3}, Ljava/io/FileInputStream;->close()V

    # v7 = new String(v6)
    new-instance v7, Ljava/lang/String;
    invoke-direct {v7, v6}, Ljava/lang/String;-><init>([B)V

    # v2, v3 = Double.parseDouble(v7.substring(0, 16))
    const/4 v2, 0x0
    const/16 v3, 0x10
    invoke-virtual {v7, v2, v3}, Ljava/lang/String;->substring(II)Ljava/lang/String;
    move-result-object v2
    invoke-static {v2}, Ljava/lang/Double;->parseDouble(Ljava/lang/String;)D
    move-result-wide v2

    # v4, v5 = Double.parseDouble(v7.substring(16, 32))
    const/16 v4, 0x10
    const/16 v5, 0x20
    invoke-virtual {v7, v4, v5}, Ljava/lang/String;->substring(II)Ljava/lang/String;
    move-result-object v4
    invoke-static {v4}, Ljava/lang/Double;->parseDouble(Ljava/lang/String;)D
    move-result-wide v4

    # p1.setLatitude(v2, v3)
    invoke-virtual {p1, v2, v3}, Landroid/location/Location;->setLatitude(D)V

    # p1.setLongitude(v4, v5)
    invoke-virtual {p1, v4, v5}, Landroid/location/Location;->setLongitude(D)V

    :cond_0

    :insert_end_0

    # =================
    # Inserted code end
    # =================

    invoke-direct {p0, p1, p2, v0}, Lcom/nianticlabs/nia/location/NianticLocationManager;->nativeLocationUpdate(Landroid/location/Location;[ILandroid/content/Context;)V

    .line 202
    monitor-exit v1

    .line 203
    return-void

    .line 202
    :catchall_0
    move-exception v0

    monitor-exit v1
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    throw v0
.end method
