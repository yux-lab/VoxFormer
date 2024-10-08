checkpoint_config = dict(interval=2)
log_config = dict(
    interval=50,
    hooks=[dict(type='TextLoggerHook'),
           dict(type='TensorboardLoggerHook')])
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './result/voxformer_batch4/msnet3d_sweep10_iou5203_resnet50_dim128_stage2_temporal'
load_from = None
resume_from = None
workflow = [('train', 1)]
plugin = True
plugin_dir = 'projects/mmdet3d_plugin/'
_num_layers_cross_ = 3
_num_points_cross_ = 8
_num_layers_self_ = 2
_num_points_self_ = 8
_dim_ = 128
_pos_dim_ = 64
_ffn_dim_ = 256
_num_levels_ = 1
_labels_tag_ = 'labels'
_num_cams_ = 5
_temporal_ = [-12, -9, -6, -3]
point_cloud_range = [0, -25.6, -2.0, 51.2, 25.6, 4.4]
voxel_size = [0.2, 0.2, 0.2]
_sem_scal_loss_ = True
_geo_scal_loss_ = True
_depthmodel_ = 'msnet3d'
_nsweep_ = 10
_query_tag_ = 'query_iou5203_pre7712_rec6153'
model = dict(
    type='VoxFormer',
    pretrained=dict(img='ckpts/resnet50-19c8e357.pth'),
    img_backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(2, ),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=False),
        norm_eval=True,
        style='pytorch'),
    img_neck=dict(
        type='FPN',
        in_channels=[1024],
        out_channels=128,
        start_level=0,
        add_extra_convs='on_output',
        num_outs=1,
        relu_before_extra_convs=True),
    pts_bbox_head=dict(
        type='VoxFormerHead',
        bev_h=128,
        bev_w=128,
        bev_z=16,
        embed_dims=128,
        CE_ssc_loss=True,
        geo_scal_loss=True,
        sem_scal_loss=True,
        cross_transformer=dict(
            type='PerceptionTransformer',
            rotate_prev_bev=True,
            use_shift=True,
            embed_dims=128,
            num_cams=5,
            encoder=dict(
                type='VoxFormerEncoder',
                num_layers=3,
                pc_range=[0, -25.6, -2.0, 51.2, 25.6, 4.4],
                num_points_in_pillar=8,
                return_intermediate=False,
                transformerlayers=dict(
                    type='VoxFormerLayer',
                    attn_cfgs=[
                        dict(
                            type='DeformCrossAttention',
                            pc_range=[0, -25.6, -2.0, 51.2, 25.6, 4.4],
                            num_cams=5,
                            deformable_attention=dict(
                                type='MSDeformableAttention3D',
                                embed_dims=128,
                                num_points=8,
                                num_levels=1),
                            embed_dims=128)
                    ],
                    ffn_cfgs=dict(
                        type='FFN',
                        embed_dims=128,
                        feedforward_channels=1024,
                        num_fcs=2,
                        ffn_drop=0.0,
                        act_cfg=dict(type='ReLU', inplace=True)),
                    feedforward_channels=256,
                    ffn_dropout=0.1,
                    operation_order=('cross_attn', 'norm', 'ffn', 'norm')))),
        self_transformer=dict(
            type='PerceptionTransformer',
            rotate_prev_bev=True,
            use_shift=True,
            embed_dims=128,
            num_cams=5,
            encoder=dict(
                type='VoxFormerEncoder',
                num_layers=2,
                pc_range=[0, -25.6, -2.0, 51.2, 25.6, 4.4],
                num_points_in_pillar=8,
                return_intermediate=False,
                transformerlayers=dict(
                    type='VoxFormerLayer',
                    attn_cfgs=[
                        dict(
                            type='DeformSelfAttention',
                            embed_dims=128,
                            num_levels=1,
                            num_points=8)
                    ],
                    ffn_cfgs=dict(
                        type='FFN',
                        embed_dims=128,
                        feedforward_channels=1024,
                        num_fcs=2,
                        ffn_drop=0.0,
                        act_cfg=dict(type='ReLU', inplace=True)),
                    feedforward_channels=256,
                    ffn_dropout=0.1,
                    operation_order=('self_attn', 'norm', 'ffn', 'norm')))),
        positional_encoding=dict(
            type='LearnedPositionalEncoding',
            num_feats=64,
            row_num_embed=512,
            col_num_embed=512)),
    train_cfg=dict(
        pts=dict(
            grid_size=[512, 512, 1],
            voxel_size=[0.2, 0.2, 0.2],
            point_cloud_range=[0, -25.6, -2.0, 51.2, 25.6, 4.4],
            out_size_factor=4,
            assigner=dict(
                type='HungarianAssigner3D',
                cls_cost=dict(type='FocalLossCost', weight=2.0),
                reg_cost=dict(type='BBox3DL1Cost', weight=0.25),
                iou_cost=dict(type='IoUCost', weight=0.0),
                pc_range=[0, -25.6, -2.0, 51.2, 25.6, 4.4]))))
dataset_type = 'SemanticKittiDatasetStage2'
data_root = './kitti/'
file_client_args = dict(backend='disk')
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=4,
    train=dict(
        type='SemanticKittiDatasetStage2',
        split='train',
        test_mode=False,
        data_root='./kitti/',
        preprocess_root='./kitti/dataset',
        eval_range=51.2,
        depthmodel='msnet3d',
        nsweep=10,
        temporal=[-12, -9, -6, -3],
        labels_tag='labels',
        query_tag='query_iou5203_pre7712_rec6153'),
    val=dict(
        type='SemanticKittiDatasetStage2',
        split='val',
        test_mode=True,
        data_root='./kitti/',
        preprocess_root='./kitti/dataset',
        eval_range=51.2,
        depthmodel='msnet3d',
        nsweep=10,
        temporal=[-12, -9, -6, -3],
        labels_tag='labels',
        query_tag='query_iou5203_pre7712_rec6153'),
    test=dict(
        type='SemanticKittiDatasetStage2',
        split='test',
        test_mode=True,
        data_root='./kitti/',
        preprocess_root='./kitti/dataset',
        eval_range=51.2,
        depthmodel='msnet3d',
        nsweep=10,
        temporal=[-12, -9, -6, -3],
        labels_tag='labels',
        query_tag='query_iou5203_pre7712_rec6153'),
    shuffler_sampler=dict(type='DistributedGroupSampler'),
    nonshuffler_sampler=dict(type='DistributedSampler'))
optimizer = dict(type='AdamW', lr=0.0002, weight_decay=0.01)
optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))
lr_config = dict(
    policy='CosineAnnealing',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.3333333333333333,
    min_lr_ratio=0.001)
total_epochs = 20
evaluation = dict(interval=1)
runner = dict(type='EpochBasedRunner', max_epochs=20)
gpu_ids = range(0, 4)
